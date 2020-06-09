from basicmonitor.triggers.trigger import Trigger
from basicmonitor.data_models import ItemManager
import threading



class EventWorker(threading.Thread):
	def __init__(self, handler, event_manager):
		self.handler = handler
		self.event_manager = event_manager
		threading.Thread.__init__(self, daemon=True)


	def run(self):
		for event in self.event_manager.subscribe():
			self.handler(event)


class TriggerManager(ItemManager):
	def __init__(self, db, sensor_manager, action_manager, event_manager):
		ItemManager.__init__(self,
			db=db,
			item_factory_function=Trigger.from_json,
			item_table_name="triggers",
		    item_name="trigger",
			reading_table_prefix="trigger-"
		)
		# other managers
		self.sensor_manager = sensor_manager
		self.action_manager = action_manager

		# set up the worker
		self.event_worker = EventWorker(self.handle_event, event_manager)
		self.event_worker.start()


	def handle_event(self, event):
		if not event["message"] == "sensor updated":
			return

		sensor_id = event["data"]["id"]
		for trigger in self.items:
			if sensor_id in trigger.linked_sensors:
				#print(f"updating {trigger.name}, because sensor {self.sensor_manager[sensor_id].name} was updated")
				try:
					trigger.update(self.sensor_manager, self.action_manager)
				except Exception as e:
					print(e)
