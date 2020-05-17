from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort

import monitor.sensors
from monitor import validators, state
from monitor.sensors import sensors_available
from monitor.api.base import DetailApi, ListCreateApi

_validation_mask = {
	"interval": validators.number_greater_than(29),
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"name": validators.string,
	"enabled": validators.boolean,
	"type": validators.whitelist(sensors_available),
	"url": validators.string,
}


class SensorDetailApi(DetailApi):
	def __init__(self):
		DetailApi.__init__(self,
			manager_provider=state.get_sensor_manager,
			validation_mask=_validation_mask
		)


class SensorApi(ListCreateApi):
	def __init__(self):

		def on_sensor_created(sensor):
			# update sensor asynchronously
			state.get_sensor_manager().updater.cmd(sensor.update)

		ListCreateApi.__init__(self,
			manager_provider=state.get_sensor_manager,
			validation_mask=_validation_mask,
		    item_class=monitor.sensors.Sensor,
			on_item_created=on_sensor_created,
		)


class SensorUpdateApi(Resource):
	def get(self, item_id):
		sensor = state.get_sensor_manager()[item_id]
		if sensor is None:
			abort(404)

		return sensor.update()

