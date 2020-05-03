from monitor.helpers import uid
from monitor.triggers import parser
import time, json

def do_nothing(*args): pass


class Trigger(object):
	def __init__(self, variables, expression, sensor_manager, **kwargs):
		# general info
		self.id = kwargs.pop("id", uid())
		self.name = kwargs.pop("name", "New Trigger")
		self.retain_for = kwargs.pop("retain_for", 90 * 24 * 60 * 60)
		self.enabled = kwargs.pop("enabled", True)

		# guts
		self._expression = expression
		self._variables = variables
		self.sensor_manager = sensor_manager
		self.broken = False
		self.validate()

		# remember linked sensors
		self.linked_sensors = []

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# events
		self.on_check = do_nothing


	def evaluate(self):
		return parser.evaluate(self.expression, self.variables, self.sensor_manager)


	def check(self):
		t = time.time()

		state = self.evaluate()
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


	def validate(self):
		assert parser.evaluate(self._expression, self._variables, self.sensor_manager) in [True, False]


	@property
	def expression(self):
		return self._expression


	@expression.setter
	def expression(self, value):
		old = self._expression
		self._expression = value
		try:
			self.validate()
		except:
			self._expression = old


	@property
	def variables(self):
		return self._variables


	@variables.setter
	def variables(self, value):
		old = self._variables
		self._variables = value
		try:
			self.validate()
		except:
			self._variables = old


	def to_dict(self):
		# Attributes of this opject, that will be serialized
		whitelist = ["id", "name", "enabled", "retain_for", "last_update", "variables", "expression"]
		attributes = {key: self.__dict__[key] for key in whitelist if key in self.__dict__}
		return attributes


	def to_json(self):
		return json.dumps(self.to_dict(), sort_keys=True)


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		return cls(**d)