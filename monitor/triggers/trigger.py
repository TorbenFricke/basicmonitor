from monitor.triggers import parser
import time

def do_nothing(*args): pass


class Trigger(object):
	def __init__(self, variables, expression, sensor_manager):
		self._expression = expression
		self._variables = variables
		self.sensor_manager = sensor_manager
		self.broken = False
		self.validate()

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

		self.on_check(state)

		return {
			"time": t,
			"state": state,
		}


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