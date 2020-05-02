from monitor.event import EventManager
from monitor.sensors import SensorManager
from monitor.db import Database
import os, threading, collections

_state = collections.defaultdict(dict)
_lock = threading.Lock()

def get_state():
	with _lock:
		if not "event_manager" in _state:
			# create Database instance
			db = Database('{}/everything.db'.format(os.path.dirname(__file__)))

			# create sensor manager
			sensor_manager = SensorManager(db)
			sensor_manager.load()

			# create event manager
			event_manager = EventManager(sensor_manager)
			_state["db"] = db
			_state["sensor_manager"] = sensor_manager
			_state["event_manager"] = event_manager

	return _state


def get_db():
	return get_state()["db"]


def get_sensor_manager():
	return get_state()["sensor_manager"]


def get_event_manager():
	return get_state()["event_manager"]