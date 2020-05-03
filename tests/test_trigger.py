from unittest import TestCase
from monitor.sensors.manager import SensorManager
from monitor.event import EventManager
from monitor.sensors import HTML, Uptime
from monitor.db import Database
from monitor.triggers import parser, trigger


def make_sensor_with_data(sensor_manager):
	sensor = Uptime()
	sensor_manager.add(sensor)
	for _ in range(100):
		sensor.update()
	return sensor


def test_context(f):
	def wrapped(self):
		db = Database(":memory:", echo=False)
		sensor_manager = SensorManager(db)
		event_manager = EventManager(sensor_manager)
		return f(self, sensor_manager, event_manager)
	return wrapped



class SensorManagerTest(TestCase):

	@test_context
	def test_evaluate_greater(self, sensor_manager, event_manager):
		id = make_sensor_with_data(sensor_manager).id
		vars = {
			"t": {"id": id, "channel": "time", "row": -1},
			"uptime": {"id": id, "channel": "seconds", "row": -1},
		}

		assert parser.evaluate("t > 4", vars, sensor_manager)
		assert parser.evaluate("t < 1e20", vars, sensor_manager)
		assert parser.evaluate("uptime < 1e20", vars, sensor_manager)
		assert parser.evaluate("uptime > 0", vars, sensor_manager)
		assert parser.evaluate("uptime < 0", vars, sensor_manager) == False
		assert parser.evaluate("uptime > 0 and t < 1e20 and 'cat' in 'bobcats' and not 'cat' in 'bobcAts'",
		                       vars, sensor_manager)


	@test_context
	def test_save_load(self, sensor_manager, event_manager):
		id = make_sensor_with_data(sensor_manager).id
		vars = {
			"t": {"id": id, "channel": "time", "row": -1},
			"uptime": {"id": id, "channel": "seconds", "row": -1},
		}

		# make a trigger
		t = trigger.Trigger(name="test", variables=vars, expression="t < 4", sensor_manager=sensor_manager)

		# serialize and deserialize
		new = trigger.Trigger.from_json(t.to_json())
		assert t.to_json() == new.to_json()

		assert t.evaluate(sensor_manager) == False
		assert t.check(sensor_manager)["state"] == False

		assert new.evaluate(sensor_manager) == False

		# change the expression
		new.expression = "t > 4"
		assert new.evaluate(sensor_manager)