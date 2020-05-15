from monitor.helpers import uid
from monitor.triggers import parser
from monitor.data_models import SerializableObject
import time, json

def do_nothing(*args): pass


class Trigger(SerializableObject):
	channels = {"state": bool}
	_serialize_blacklist = ["broken", "_variables", "linked_sensors", "on_check", "update_handler"]

	def __init__(self, variables=None, expression="", **kwargs):
		# general info
		self.id = kwargs.pop("id", uid())
		self.name = kwargs.pop("name", "New Trigger")
		self.retain_for = kwargs.pop("retain_for", 90 * 24 * 60 * 60)
		self.enabled = kwargs.pop("enabled", True)

		# remember linked sensors
		self.linked_sensors = set()

		# guts
		self.expression = expression
		self._variables = None
		# sensors will be linked when setting the variables using the setter method
		self.variables = variables
		self.broken = False

		# update handler function
		self.update_handler = do_nothing

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# events
		self.on_check = do_nothing


	def evaluate(self, sensor_manager):
		return parser.evaluate(self.expression, self.variables, sensor_manager)


	def check(self, sensor_manager):
		t = time.time()

		state = self.evaluate(sensor_manager)
		if not state in [True, False]:
			self.broken = True
			return

		# remember the last update
		self.last_update = t

		info = {
			"time": t,
			"state": state,
		}

		# event
		self.on_check(info)

		return info


	@property
	def variables(self):
		return self._variables


	@variables.setter
	def variables(self, value):
		self._variables = value
		self.linked_sensors = set()
		for variable in value.values():
			self.linked_sensors.add(variable["id"])


	def to_dict(self):
		out = SerializableObject.to_dict(self)
		out["variables"] = self.variables
		return out