from unittest import TestCase
from monitor.sensors.host_system import *
from monitor.sensors.web import *
from monitor.sensors.base import Sensor
from monitor.sensors import sensors_available

host_system_sensors = [RAMPercentage, CPUPercentage, Uptime]


class SensorTest(TestCase):

	def test_host_system(self):
		for cls in host_system_sensors:
			sensor = cls()
			self.assertTrue(type(sensor.fetch()) is float)

			update = sensor.update()
			if "percentage" in cls.__name__.lower():
				self.assertEqual(len(update), 2)
				self.assertTrue(0 <= update["percentage"] <= 100)


	def test_serialize_deserialize(self):
		for name, cls in Sensor.subclasses_by_name().items():
			sensor = cls(name="test", interval=7612, cat="dog", url="woof")
			js = sensor.to_json()
			new_sensor = Sensor.from_json(js)
			new_js = new_sensor.to_json()
			self.assertEqual(js, new_js)


	def test_HTML(self):
		# do we get an error if we do not provide a url?
		self.assertRaises(KeyError, HTML)

		s = HTML(url="http://google.com")
		data = s.fetch()
		self.assertGreater(data["elapsed"], 0)