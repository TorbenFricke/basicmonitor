from unittest import TestCase
from queue import Queue, Empty
from threading import Thread
import time
from basicmonitor.db import Database
from basicmonitor.sensors import SensorManager
from basicmonitor.event import EventManager
from basicmonitor.sensors import Uptime


class YieldTestThread(Thread):
	def __init__(self, target):
		self.error_queue = Queue()
		self.target = target
		self.no_calls = 0
		Thread.__init__(self, daemon=True)


	def run(self):
		try:
			for txt in self.target():
				print(txt)
				self.no_calls += 1
		except Exception as e:
			self.error_queue.put(e)


	def raise_errors(self):
		# raise any errors in main thread
		try:
			raise self.error_queue.get_nowait()
		except Empty:
			pass



def test_context(f):
	def wrapped(self):
		db = Database(":memory:", echo=False)
		sensor_manager = SensorManager(db)
		event_manager = EventManager(sensor_manager)
		return f(self, sensor_manager, event_manager)
	return wrapped


class SensorManagerTest(TestCase):

	@test_context
	def test_add_and_delete_sensor(self, sensor_manager, event_manager):
		t = YieldTestThread(event_manager.subscribe)
		t.start()

		sensor_manager.add(Uptime())
		sensor_manager.add(Uptime())
		sensor_manager.add(Uptime())
		sensor_manager.add(Uptime())
		sensor_manager.delete(sensor_manager.items[2].id)
		time.sleep(0.2)

		assert t.no_calls == 5
		t.raise_errors()


	@test_context
	def test_update_sensor(self, sensor_manager, event_manager):
		t = YieldTestThread(event_manager.subscribe)
		t.start()

		sensor_manager.add(Uptime())
		sensor_manager.updater.check_sensors()
		# sensor should not be updated again, as it was just updated
		sensor_manager.updater.check_sensors()
		time.sleep(0.2)

		assert t.no_calls == 2
		t.raise_errors()


	@test_context
	def test_cleanup(self, sensor_manager, event_manager):
		# make a real thread
		t = YieldTestThread(event_manager.subscribe)
		t.start()

		time.sleep(0.2)

		# a made up thread
		dummy = "dummy thread key"
		_ = event_manager.subscriptions[dummy]

		event_manager.cleanup_dead_threads()

		assert not dummy in event_manager.subscriptions
		assert t.ident in event_manager.subscriptions