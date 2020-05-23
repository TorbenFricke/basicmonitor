from monitor.helpers import uid
from monitor.triggers import parser
from monitor.data_models import SerializableObject
import time, json

def do_nothing(*args): pass


class Trigger(SerializableObject):
	channels = {"state": bool}
	_serialize_blacklist = ["on_check", "update_handler"]

	def __init__(self, variables=None, expression="", **kwargs):
		# general info
		self.id = kwargs.pop("id", uid())
		self.name = kwargs.pop("name", "New Trigger")
		self.retain_for = kwargs.pop("retain_for", 90 * 24 * 60 * 60)
		self.enabled = kwargs.pop("enabled", True)


		# guts
		self.expression = expression
		self.variables = variables
		self.broken = False

		# update handler
		self.update_handler = do_nothing

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)



	def evaluate(self, sensor_manager):
		return parser.evaluate(self.expression, self.variables, sensor_manager)


	def update(self, sensor_manager):
		t = time.time()

		try:
			state = self.evaluate(sensor_manager)
			assert state in [True, False]
			self.broken = False
		except:
			self.broken = True
			state = None

		# remember the last update
		self.last_update = t

		reading = {
			"time": t,
			"state": state,
		}

		# event
		self.update_handler(self.id, reading)

		return reading


	@property
	def linked_sensors(self):
		return set([variable["id"] for variable in self.variables.values()])


	def to_dict(self):
		out = SerializableObject.to_dict(self)
		return out