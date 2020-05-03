from monitor.helpers import uid
from monitor.triggers import parser
import time, json

def do_nothing(*args): pass


class Trigger(object):
	def __init__(self, variables=None, expression="", **kwargs):
		# general info
		self.id = kwargs.pop("id", uid())
		self.name = kwargs.pop("name", "New Trigger")
		self.retain_for = kwargs.pop("retain_for", 90 * 24 * 60 * 60)
		self.enabled = kwargs.pop("enabled", True)

		# guts
		self.expression = expression
		self._variables = variables
		self.broken = False

		# remember linked sensors
		self.linked_sensors = set()

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
		for variable in value:
			self.linked_sensors.add(variable["id"])


	def to_dict(self):
		# Attributes of this opject, that will be serialized
		whitelist = ["id", "name", "enabled", "retain_for", "last_update", "expression"]
		attributes = {key: self.__dict__[key] for key in whitelist if key in self.__dict__}
		attributes["variables"] = self.variables
		return attributes


	def to_json(self):
		return json.dumps(self.to_dict(), sort_keys=True)


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		return cls(**d)