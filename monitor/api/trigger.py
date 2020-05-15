from flask_restful import Resource, request

from monitor import validators, state
from monitor import sensors
from monitor.triggers import Trigger


def make_variables_validator():
	all_channels = ["time"] + [cls.channels.keys() for cls in sensors.Sensor.__subclasses__()]
	variables_mask = {
		"id": validators.string,
		"row": validators.integer,
		"channel": validators.whitelist(all_channels),
	}

	def wrapped(variables):
		out = {}
		for key, var in variables.items():
			clean = validators.apply_validation_mask(var, variables_mask)

			# make sure all information for a variable is present
			for key in variables_mask.keys():
				assert key in clean

			out[key] = clean

		return out

	return wrapped



_validation_mask = {
	"name": validators.string,
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"expression": validators.string,
	"variables": make_variables_validator()
}


# list and create triggers
class TriggerApi(Resource):
	def get(self):
		return [trigger.to_dict() for trigger in state.get_trigger_manager().triggers]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, _validation_mask)

			# make the trigger
			trigger = Trigger(**clean)

		except Exception as e:
			return {"message": str(e)}

		trigger_manager = state.get_trigger_manager()
		trigger_manager.add(trigger )

		return trigger .to_dict()



# trigger detail
class TriggerDetailApi(Resource):
	def get(self, trigger_id):
		return state.get_trigger_manager()[trigger_id].to_dict()