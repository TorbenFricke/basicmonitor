import threading, queue, time
from basicmonitor.helpers import do_nothing

class UpdateWorker(threading.Thread):
	def __init__(self, parent, time_to_update_function, update_function=lambda item: item.update()):
		threading.Thread.__init__(self)
		self.daemon = True
		self.command_queue = queue.Queue()
		self.parent = parent

		self.update_function = update_function
		self.time_to_update_function = time_to_update_function

		# events
		self.on_update = do_nothing


	def check_sensors(self):
		next_timeout = 5
		for item in self.parent.items:
			# ignore all disabled sensors
			if not item.enabled:
				continue
			time_to_update = self.time_to_update_function(item)
			# update sensor
			if time_to_update <= 0:
				self.update_function(item)
			# remember lowest time remaining - this makes sure, we do not wait too long and pass an update
			if time_to_update < next_timeout: next_timeout = time_to_update
			# also make sure we do not wait longer, than the smallest interval
			if item.interval < next_timeout: next_timeout = item.interval

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
