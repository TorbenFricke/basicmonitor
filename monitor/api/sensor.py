from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort

import monitor.sensors
from monitor import validators, state
from monitor.sensors import sensors_available

_validation_mask = {
	"interval": validators.number_greater_than(29),
	"retain_for": validators.number_greater_than(60*60), # at lesat one hour
	"name": None,
	"enabled": validators.boolean,
	"type": validators.whitelist(sensors_available),
	"url": None,
}


class SensorDetailApi(Resource):
	def get(self, sensor_id):
		sensor_manager = state.get_sensor_manager()
		sensor = sensor_manager[sensor_id]
		if sensor is None:
			abort(404)

		data = sensor.to_dict()
		data["last_reading"] = sensor_manager.last_reading(sensor_id)
		return data


	def delete(self, sensor_id):
		state.get_sensor_manager().delete(sensor_id)
		return "deleted {}".format(sensor_id)


	def put(self, sensor_id):
		sensor = state.get_sensor_manager()[sensor_id]
		if sensor is None:
			abort(404)

		data = request.get_json(force=True)
		try:
			clean = validators.apply_validation_mask(data, _validation_mask)
			kwargs = sensor.kwargs
			for key, value in clean.items():
				if key in sensor.__dict__:
					setattr(sensor, key, value)
				if key in kwargs:
					kwargs[key] = value

			# trigger event
			state.get_event_manager().on_sensor_edit(sensor.id)

		except Exception as e:
			return {"message": str(e)}

		return sensor.to_dict()


class SensorApi(Resource):
	def get(self):
		return [sensor.to_dict() for sensor in state.get_sensor_manager().items]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, _validation_mask)

			# make the sensor
			cls = monitor.sensors.Sensor.subclasses_by_name()[clean.pop("type")]
			sensor = cls(**clean)

		except Exception as e:
			return {"message": str(e)}

		sensor_manager = state.get_sensor_manager()
		sensor_manager.add(sensor)
		# update sensor asynchronously
		sensor_manager.updater.cmd(sensor.update)
		return sensor.to_dict()


class SensorDeleteUpdateApi(Resource):
	def get(self, sensor_id):
		sensor = state.get_sensor_manager()[sensor_id]
		if sensor is None:
			abort(404)

		return sensor.update()


	def delete(self, sensor_id):
		state.get_sensor_manager().delete(sensor_id)
		return "delted {}".format(sensor_id)


