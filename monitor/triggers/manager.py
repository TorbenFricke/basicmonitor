from monitor.triggers.trigger import Trigger
from monitor.data_models import ItemManager
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


class TriggerManager(ItemManager):
	def __init__(self, db, sensor_manager, event_manager):
		ItemManager.__init__(self,
			db=db,
			item_factory_function=Trigger.from_json,
			item_table_name="triggers",
			reading_table_prefix="trigger-"
		)
		# other managers
		self.sensor_manager = sensor_manager
		self.event_manager = event_manager

		# set up the worker
		self.event_worker = EventWorker(self)
		self.event_worker.start()


	def handle_event(self, event):
		if not event.message == "sensor updated":
			return

		sensor_id = event.id
		for trigger in self.items:
			if sensor_id in trigger.linked_sensors:
				trigger.check(self.sensor_manager)
