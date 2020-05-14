import json, threading, time


class SerializableObject(object):
	_serialize_blacklist = ["update_handler"]
	"""Attributes of this object, that will not be serialized"""


	def to_dict(self):
		return {key: value for key, value in self.__dict__.items() if key not in self._serialize_blacklist}


	def to_json(self):
		return json.dumps(self.to_dict(), sort_keys=True)


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		return cls(**d)



def do_nothing(*args): pass



class RemoveOldReadingsWorker(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.daemon = True
		self.parent: ItemManager = parent

	def remove_old_values(self):
		db = self.parent.db
		now = time.time()
		for item in self.parent.items:
			prefix = self.parent.readings_table_prefix
			older_than = now - item.retain_for
			db.remove_old_readings(prefix + item.id, older_than)

	def run(self):
		while True:
			time.sleep(5*60)
			try:
				self.remove_old_values()
			except:
				pass


class ItemManager(object):
	def __init__(self, db, item_table_name, reading_table_prefix, item_factory_function):
		self.items = []
		self.db = db
		self.item_table = db.object_table(item_table_name)
		self.readings_table_prefix = reading_table_prefix
		self.item_factory_function = item_factory_function

		# events
		self.on_add_item = do_nothing
		self.on_delete_item = do_nothing
		self.on_update = do_nothing

		# remove old database entries worker
		self.remove_old_worker = RemoveOldReadingsWorker(self)
		self.remove_old_worker.start()


	def add(self, item):
		# overwrite old item with same UID
		for i in self.items:
			if item.id == i.id:
				self.delete(i.id)
		# append new item
		self.items.append(item)
		self.link_item(item)

		self.save()

		# trigger event
		self.on_add_item(item.to_dict())


	def link_item(self, item):
		# make and link corresponding DB table
		self.db.channel_table(item, self.readings_table_prefix)

		def update_handler(id, reading):
			self.db.insert_reading(id, reading, self.readings_table_prefix)
			self.on_update({
				"id": id,
				#"reading": reading # including the reading may cause the json parser to fail for large readings....
			})

		# handle updates
		item.update_handler = update_handler


	def delete(self, uid):
		for i, s in enumerate(self.items):
			if not s.id == uid:
				continue
			# found the item
			del self.items[i]
			# remove corresponding DB table
			self.db.delete_id(self.item_table, uid)
			self.db.drop(self.readings_table_prefix + uid)

			# trigger event
			self.on_delete_item(uid)

			return True
		return False


	def last_reading(self, uid):
		readings = self.db.fetch_last_reading(self.readings_table_prefix + uid)
		if len(readings) > 0:
			return readings[-1]


	def save(self):
		self.db.save_objects(self.item_table, self.items)


	def load(self):
		self.items = self.db.load_objects(self.item_table, self.item_factory_function)
		for item in self.items:
			self.link_item(item)


	def __getitem__(self, uid):
		for item in self.items:
			if uid == item.id:
				return item