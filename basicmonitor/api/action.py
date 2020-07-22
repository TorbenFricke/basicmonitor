from flask_restful import Resource
from werkzeug.exceptions import abort
from flask import request

import basicmonitor.actions
from basicmonitor import validators, state
from basicmonitor.actions import actions_available
from basicmonitor.api.base import DetailApi, ListCreateApi, ErrorResponse

_validation_mask = {
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"name": validators.non_empty_string,
	"enabled": validators.boolean,
	"cooldown": validators.positive_float,
	"type": validators.conditional_validator(
		validators.whitelist(actions_available),
		{
			'PushoverAction': {
				"api_token": validators.non_empty_string,
				"user_key": validators.non_empty_string,
				"device": validators.non_empty_string,
			},
			'WebhookAction': {
				"url": validators.non_empty_string,
				"method": validators.whitelist(["get", "put", "post", "delete"],
				                               preprocessor=lambda x: str(x).lower()),
			},
			'RebootAction': {},
		}
	),
}


class ActionDetailApi(DetailApi):
	def __init__(self):
		DetailApi.__init__(self,
			manager_provider=state.get_action_manager,
			validation_mask=_validation_mask
		)


class ActionApi(ListCreateApi):
	def __init__(self):
		ListCreateApi.__init__(self,
		                       manager_provider=state.get_action_manager,
		                       validation_mask=_validation_mask,
		                       item_class=basicmonitor.actions.Action,
		                       )


class ActionNotifyApi(Resource):
	def post(self, item_id):
		action = state.get_action_manager()[item_id]
		if action is None:
			return ErrorResponse("Item not found")

		try:
			# do some validation
			data = request.get_json(force=True)
			message = data.get("message", "No message provided")
			assert type(message) == str
			force_send = data.get("force_send", False)
			assert type(force_send) == bool

			# do the action
			response = action.notify(message, force_send)

		except Exception as e:
			return ErrorResponse(e)

		return response
