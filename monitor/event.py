from queue import Queue
import collections, threading


class EventManager(object):
	def __init__(self, sensor_manager):
		self.sensor_manager = sensor_manager
		self.sensor_manager.on_add_sensor = self._basic_on_event_handler("sensor added")
		self.sensor_manager.on_delete_sensor = self._basic_on_event_handler("sensor deleted")
		self.sensor_manager.on_update = self._basic_on_event_handler("sensor updated")

		# to be called manually
		self.on_sensor_edit = self._basic_on_event_handler("sensor edited")

		self.subscriptions = collections.defaultdict(Queue)


	def cleanup_dead_threads(self):
		threads_alive = [thread.ident for thread in threading.enumerate()]
		for key in list(self.subscriptions.keys()):
			if not key in threads_alive:
				del self.subscriptions[key]


	def subscribe(self):
		self.cleanup_dead_threads()
		thread_id = threading.get_ident()
		q = self.subscriptions[thread_id]
		while True:
			yield q.get()


	def _basic_on_event_handler(self, message):
		def on_event_handler(arg):
			data = {
				"message": message,
				"data": arg
			}

			for queue in self.subscriptions.values():
				queue.put(data)

		return on_event_handler
