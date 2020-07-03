from basicmonitor.sensors import Sensor
from basicmonitor.data_models import ItemManager, UpdateWorker
import time

class SensorManager(ItemManager):
	def __init__(self, db):
		ItemManager.__init__(self,
		                     db=db,
		                     item_table_name="sensors",
		                     reading_table_prefix="sensor-",
		                     item_name="sensor",
		                     item_factory_function=Sensor.from_json
		                     )
		self.updater = UpdateWorker(
			self,
			time_to_update_function=lambda item: item.last_update + item.interval - time.time(),
		)
		self.updater.start()

