import threading, queue, time
from monitor.sensors import Sensor
from monitor.data_models import ItemManager

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
		for sensor in self.parent.items:
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


class SensorManager(ItemManager):
	def __init__(self, db):
		ItemManager.__init__(self,
		                     db=db,
		                     item_table_name="sensors",
		                     reading_table_prefix="sensor-",
		                     item_factory_function=Sensor.from_json
		                     )
		self.updater = UpdateWorker(self)
		self.updater.start()

