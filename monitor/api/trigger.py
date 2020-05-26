from flask_restful import Resource, request, abort

from monitor import validators, state
from monitor import sensors
from monitor.triggers import Trigger
from monitor.api.base import DetailApi, ListCreateApi


# make the custom variables validator
_all_channels = ["time"]
for cls in sensors.Sensor.__subclasses__():
	_all_channels += list(cls.channels.keys())
_variables_validation_mask = {
	"id": validators.string,
	"row": validators.integer,
	"channel": validators.whitelist(_all_channels),
}

def variables_validator(variables):
	out = {}
	for variable_name, var in variables.items():
		clean = validators.apply_validation_mask(var, _variables_validation_mask)

		# make sure all information for a variable is present
		for key in _variables_validation_mask.keys():
			assert key in clean

		out[variable_name] = clean

	return out




_validation_mask = {
	"name": validators.string,
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"expression": validators.string,
	"variables": variables_validator
}


# list and create triggers
class TriggerApi(ListCreateApi):
	def __init__(self):

		def on_trigger_created(trigger):
			# update sensor synchronously
			trigger.update(state.get_sensor_manager())

		ListCreateApi.__init__(self,
			manager_provider=state.get_trigger_manager,
			validation_mask=_validation_mask,
		    item_class=Trigger,
		    on_item_created=on_trigger_created
		)


# trigger detail
class TriggerDetailApi(DetailApi):
	def __init__(self):
		DetailApi.__init__(self,
			manager_provider=state.get_trigger_manager,
			validation_mask=_validation_mask
		)


# update trigger
class TriggerUpdateApi(Resource):
	def get(self, item_id):
		trigger = state.get_trigger_manager()[item_id]
		if trigger is None:
			abort(404)

		return trigger.update(state.get_sensor_manager())