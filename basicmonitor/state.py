from basicmonitor.event import EventManager
from basicmonitor.sensors import SensorManager
from basicmonitor.triggers import TriggerManager
from basicmonitor.actions import ActionManager
from basicmonitor.db import Database
import os, threading, collections, pathlib


_state = {}
_lock = threading.Lock()

def get_state():
	with _lock:
		if not "event_manager" in _state:
			# create Database instance
			db_dir = os.path.expanduser("~/basicmonitor")
			pathlib.Path(db_dir).mkdir(parents=True, exist_ok=True)
			db = Database('{}/basicmonitor.db'.format(db_dir))

			# create sensor manager
			sensor_manager = SensorManager(db)
			sensor_manager.load()

			# create action manager
			action_manager = ActionManager(db=db)
			action_manager.load()

			# create event manager
			event_manager = EventManager(sensor_manager, action_manager)

			# create trigger manager
			trigger_manager = TriggerManager(
				db=db,
				sensor_manager=sensor_manager,
				event_manager=event_manager,
				action_manager=action_manager
			)
			trigger_manager.load()
			event_manager.link_manager(trigger_manager)

			_state["db"] = db
			_state["sensor_manager"] = sensor_manager
			_state["event_manager"] = event_manager
			_state["trigger_manager"] = trigger_manager
			_state["action_manager"] = action_manager

	return _state


def get_db() -> Database:
	return get_state()["db"]


def get_sensor_manager() -> SensorManager:
	return get_state()["sensor_manager"]


def get_event_manager() -> EventManager:
	return get_state()["event_manager"]


def get_trigger_manager() -> TriggerManager:
	return get_state()["trigger_manager"]


def get_action_manager() -> ActionManager:
	return get_state()["action_manager"]