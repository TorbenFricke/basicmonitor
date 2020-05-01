import collections, threading, queue, time
from monitor.sensors import sensors_available, Sensor

def do_nothing(*args): pass


class UpdateWorker(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.daemon = True
		self.command_queue = queue.Queue()
		self.updated_queue = queue.Queue()
		self.parent = parent

		# events
		self.on_update = do_nothing


	def check_sensors(self):
		now = time.time()
		next_timeout = 5
		for sensor in self.parent.sensors:
			# ignore all disabled sensors
			if not sensor.enabled:
				continue
			time_to_update = sensor.last_update + sensor.interval - now
			# update sensor
			if time_to_update <= 0:
				sensor.update()
			# remember lowest time remaining - this makes sure, we do not wait too long and pass an update
			if time_to_update < next_timeout: next_timeout = time_to_update
			# also make sure we do not wait longer, than the smallest interval
			if sensor.interval < next_timeout: next_timeout = sensor.interval

		return next_timeout


	def run(self):
		next_timeout = 5
		while True:
			# execute commands commands
			try:
				cmd, args, kwargs = self.command_queue.get(timeout=next_timeout)
				cmd(*args, **kwargs)
			except:
				pass
			# update all the sensors
			try:
				next_timeout = self.check_sensors()
			except Exception as e:
				next_timeout = 5


	def cmd(self, f, *args, **kwargs):
		self.command_queue.put((f, args, kwargs))


class SensorManager(object):
	def __init__(self, db):
		self.sensors = []
		self.db = db
		self.sensors_table = db.object_table("sensors")
		self.updater = UpdateWorker(self)
		self.updater.start()

		# events
		self.on_add_sensor = do_nothing
		self.on_delete_sensor = do_nothing
		self.on_update = do_nothing


	def add(self, sensor):
		# overwrite old sensor with same UID
		for s in self.sensors:
			if sensor.id == s.id:
				self.delete(s.id)
		# append new sensor
		self.sensors.append(sensor)
		self.link_sensor(sensor)

		self.save()

		# trigger event
		self.on_add_sensor(sensor.to_flat_dict())


	def link_sensor(self, sensor):
		# make and link corresponding DB table
		self.db.channel_table(sensor)

		def update_handler(id, reading):
			self.db.insert_reading(id, reading)
			self.on_update({
				"id": id,
				#"reading": reading # including the reading may cause the json parser to fail for large readings....
			})

		# handle updates
		sensor.update_handler = update_handler


	def delete(self, uid):
		for i, s in enumerate(self.sensors):
			if not s.id == uid:
				continue
			# found the sensor
			del self.sensors[i]
			# remove corresponding DB table
			self.db.delete_id(self.sensors_table, uid)
			self.db.drop(self.db.sensor_prefix + uid)

			# trigger event
			self.on_delete_sensor(uid)

			return True
		return False


	def last_reading(self, uid):
		readings = self.db.fetch_last_reading(self.db.sensor_prefix + uid)
		if len(readings) > 0:
			return readings[-1]


	def save(self):
		self.db.save_objects(self.sensors_table, self.sensors)


	def load(self):
		self.sensors = self.db.load_objects(self.sensors_table, Sensor.from_json)
		for sensor in self.sensors:
			self.link_sensor(sensor)


	def __getitem__(self, uid):
		for s in self.sensors:
			if uid == s.id:
				return s