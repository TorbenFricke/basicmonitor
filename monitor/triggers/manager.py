from monitor.triggers.trigger import Trigger
import threading



class EventWorker(threading.Thread):
	def __init__(self, parent):
		self.parent = parent
		threading.Thread.__init__(self, daemon=True)


	def run(self):
		for event in self.parent.event_manager.subscribe():
			try:
				self.parent.handle_event(event)
			except:
				pass


class TriggerManager(object):
	def __init__(self, db, sensor_manager, event_manager):
		self.db = db
		self.sensor_manager = sensor_manager
		self.event_manager = event_manager

		# set up the database
		self.trigger_table = db.object_table("triggers")

		# list of triggers
		self.triggers = []

		# set up the worker
		self.event_worker = EventWorker(self)
		self.event_worker.start()


	def add(self, trigger: Trigger):
		self.link_trigger(trigger)
		self.triggers.append(trigger)


	def link_trigger(self, trigger):
		# TODO events, database
		pass


	def handle_event(self, event):
		if not event.message == "sensor updated":
			return

		sensor_id = event.id
		for trigger in self.triggers:
			if sensor_id in trigger.linked_sensors:
				trigger.check(self.sensor_manager)


	def save(self):
		self.db.save_objects(self.trigger_table, self.triggers)


	def load(self):
		self.triggers = self.db.load_objects(self.trigger_table, Trigger.from_json)
		for trigger in self.triggers:
			self.link_trigger(trigger)