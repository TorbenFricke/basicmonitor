from flask_restful import Resource, request, abort

from basicmonitor import validators, state
from basicmonitor import sensors
from basicmonitor.triggers import Trigger
from basicmonitor.api.base import DetailApi, ListCreateApi, ErrorResponse


# make the custom variables validator
_all_channels = ["time"]
for cls in sensors.Sensor.__subclasses__():
	_all_channels += list(cls.channels.keys())
_variables_validation_mask = {
	"variable": validators.string,
	"id": validators.string,
	"row": validators.integer,
	"channel": validators.whitelist(_all_channels),
}

def variables_validator(variables):
	return [
		validators.apply_validation_mask(var, _variables_validation_mask) for var in variables
	]


_validation_mask = {
	"name": validators.string,
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"expression": validators.string,
	"variables": variables_validator,
	"action_ids": validators.list_validator(validators.string),
	"message": validators.string,
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

	def get(self):
		# override trigger list method to include the last reading
		items = [item.to_dict() for item in self.manager_provider().items]
		for item in items:
			item["last_reading"] = self.manager_provider().last_reading(item["id"])
		return items


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
			return ErrorResponse("Item not found")

		return trigger.update(state.get_sensor_manager(), state.get_action_manager())