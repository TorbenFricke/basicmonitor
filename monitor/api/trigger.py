from flask_restful import Resource, request, abort

from monitor import validators, state
from monitor import sensors
from monitor.triggers import Trigger


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
class TriggerApi(Resource):
	def get(self):
		return [trigger.to_dict() for trigger in state.get_trigger_manager().items]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, _validation_mask)

			# make the trigger
			trigger = Trigger(**clean)

		except Exception as e:
			return {"message": str(e)}

		trigger_manager = state.get_trigger_manager()
		trigger_manager.add(trigger)

		return trigger.to_dict()



# trigger detail
class TriggerDetailApi(Resource):
	def get(self, trigger_id):
		return state.get_trigger_manager()[trigger_id].to_dict()


	def delete(self, trigger_id):
		state.get_trigger_manager().delete(trigger_id)
		return "deleted {}".format(trigger_id)


	def put(self, trigger_id):
		trigger = state.get_trigger_manager()[trigger_id]
		if trigger is None:
			abort(404)

		data = request.get_json(force=True)
		try:
			clean = validators.apply_validation_mask(data, _validation_mask)
			for key, value in clean.items():
				if key in trigger.__dict__:
					setattr(trigger, key, value)

			# trigger event
			state.get_event_manager().on_trigger_edit({"id": trigger.id})

		except Exception as e:
			return {"message": str(e)}

		return trigger.to_dict()


# update trigger
class TriggerUpdateApi(Resource):
	def get(self, trigger_id):
		trigger = state.get_trigger_manager()[trigger_id]
		if trigger is None:
			abort(404)

		return trigger.update(state.get_sensor_manager())