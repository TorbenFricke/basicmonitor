from monitor.triggers import parser
from monitor.data_models import SerializableObject
import time, json

def do_nothing(*args): pass


class Trigger(SerializableObject):
	channels = {"state": bool}

	def __init__(self, variables=None, expression="", **kwargs):
		# guts
		self.expression = expression
		self.variables = variables

		# update handler
		self.update_handler = do_nothing

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# initialize superclass, which sets all the basic things
		SerializableObject.__init__(self, **kwargs)



	def evaluate(self, sensor_manager):
		return parser.evaluate(self.expression, self.variables, sensor_manager)


	def update(self, sensor_manager):
		t = time.time()

		try:
			state = self.evaluate(sensor_manager)
			assert state in [True, False]
		except:
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