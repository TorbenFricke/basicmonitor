from basicmonitor.triggers import parser
from basicmonitor.data_models import Item
import time

def do_nothing(*args): pass


class Trigger(Item):
	channels = {"state": bool}

	def __init__(self, variables=None, expression="", message="", **kwargs):
		# guts
		self.expression = expression
		self.variables = variables
		self.message = message
		self.action_ids = list(set(kwargs.pop("action_ids", [])))
		for alert_id in self.action_ids:
			if not type(alert_id) is str:
				raise TypeError("alert id {} is not a string".format(alert_id))

		# update handler
		self.update_handler = do_nothing

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# initialize superclass, which sets all the basic things
		Item.__init__(self, **kwargs)



	def evaluate(self, sensor_manager):
		return parser.evaluate(self.expression, self.variables, sensor_manager)


	def update(self, sensor_manager, action_manager):
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

		# actions
		self._trigger_actions(action_manager)

		return reading


	def _trigger_actions(self, action_manager):
		message = f"Trigger {self.name}: {self.message}"
		for action_id in self.action_ids:
			action = action_manager[action_id]
			if action is None:
				return
			action.notify(message)


	@property
	def linked_sensors(self):
		return set([variable["id"] for variable in self.variables])


	def to_dict(self):
		out = Item.to_dict(self)
		return out