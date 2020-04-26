from flask_restful import Resource
from flask import abort, request
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


	def delete(self, sensor_id):
		sensor_manager.delete(sensor_id)
		return "delted {}".format(sensor_id)


class SensorUpdateApi(Resource):
	def get(self, sensor_id):
		sensor = sensor_manager[sensor_id]
		if sensor is None:
			abort(404)

		return sensor.update()


	def delete(self, sensor_id):
		sensor_manager.delete(sensor_id)
		return "delted {}".format(sensor_id)


from monitor import validators

_validation_mask = {
	"interval": validators.positive_float,
	"name": None,
	"enabled": validators.boolean,
	"type": validators.whitelist(sensors_available),
	"url": validators.url_safe,
}


class SensorApi(Resource):
	def get(self):
		return [sensor.to_dict() for sensor in sensor_manager.sensors]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, _validation_mask)

			# make the sensor
			cls = monitor.sensors.Sensor.subclasses_by_name()[clean.pop("type")]
			sensor = cls(**clean)

		except Exception as e:
			return {"message": str(e)}

		sensor_manager.add(sensor)
		# update sensor asynchronously
		sensor_manager.updater.cmd(sensor.update)
		return sensor.to_dict()



class DebugAddSensor(Resource):
	def get(self):
		s = monitor.sensors.HTML("facebook", url="http://facebook.com")
		sensor_manager.add(s)
		s.update()
		return s.to_dict()