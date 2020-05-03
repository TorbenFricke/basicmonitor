from flask_restful import Resource, request

from monitor import validators, state
from monitor import sensors
from monitor.triggers import Trigger


def make_variables_validator():
	all_channels = [cls.channels.keys() for cls in sensors.Sensor.__subclasses__()]
	variables_mask = {
		"id": None,
		"row": None,
		"channel": validators.whitelist(all_channels),
	}

	def wrapped(var_list):
		out = []
		for var in var_list:
			clean = validators.apply_validation_mask(var, variables_mask)
			for key in variables_mask.keys():
				assert key in clean

			out.append(clean)

		return out

	return wrapped



_validation_mask = {
	"name": None,
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"expression": None,
	"variables": make_variables_validator()
}



class TriggerApi(Resource):
	def get(self):
		return [trigger.to_dict() for trigger in state.get_trigger_manager().triggers]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, _validation_mask)

			# make the trigger
			cls = Trigger(**clean)

		except Exception as e:
			return {"message": str(e)}

		trigger_manager = state.get_trigger_manager()
		trigger_manager.add(cls)

		return cls.to_dict()

