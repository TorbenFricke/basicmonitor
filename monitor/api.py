from flask_restful import Resource
from flask import abort
import monitor.sensors
from monitor.sensors import sensors_available


# create Database instance
from monitor.db import Database
import os
db = Database('{}/everything.db'.format(os.path.dirname(__file__)))

# create sensor manager
from monitor.sensors import SensorManager
sensor_manager = SensorManager(db)
sensor_manager.load()


class SensorDetailApi(Resource):
	def get(self, sensor_id):
		sensor = sensor_manager[sensor_id]
		if sensor is None:
			abort(404)

		data = sensor.to_dict()
		data["last_reading"] = sensor_manager.last_reading(sensor_id)
		return data


class SensorApi(Resource):
	def get(self):
		return [sensor.to_dict() for sensor in sensor_manager.sensors]


	def post(self):
		# make a dummy sensor
		sensor = monitor.sensors.Uptime()
		sensor_manager.add(sensor)
		return sensor.to_dict()


class DebugAddSensor(Resource):
	def get(self):
		s = monitor.sensors.HTML("facebook", url="http://facebook.com")
		sensor_manager.add(s)
		s.update()
		return s.to_dict()