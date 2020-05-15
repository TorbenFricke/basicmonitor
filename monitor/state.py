from monitor.event import EventManager
from monitor.sensors import SensorManager
from monitor.triggers import TriggerManager
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

			# create trigger manager
			trigger_manager = TriggerManager(db=db, sensor_manager=sensor_manager, event_manager=event_manager)
			trigger_manager.load()
			event_manager.link_manager(trigger_manager)

			_state["db"] = db
			_state["sensor_manager"] = sensor_manager
			_state["event_manager"] = event_manager
			_state["trigger_manager"] = trigger_manager

	return _state


def get_db() -> Database:
	return get_state()["db"]


def get_sensor_manager() -> SensorManager:
	return get_state()["sensor_manager"]


def get_event_manager() -> EventManager:
	return get_state()["event_manager"]


def get_trigger_manager() -> TriggerManager:
	return get_state()["trigger_manager"]