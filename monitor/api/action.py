from flask_restful import Resource
from werkzeug.exceptions import abort
from flask import request

import monitor.actions
from monitor import validators, state
from monitor.actions import actions_available
from monitor.api.base import DetailApi, ListCreateApi

_validation_mask = {
	"retain_for": validators.number_greater_than(60*60), # at least one hour
	"name": validators.string,
	"enabled": validators.boolean,
	"type": validators.whitelist(actions_available),
	"cooldown": validators.positive_float,
	# Pushover
	"api_token": validators.string,
	"user_key": validators.string,
	"device": validators.string,
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
		    item_class=monitor.actions.Action,
		)


class ActionNotifyApi(Resource):
	def post(self, item_id):
		action = state.get_action_manager()[item_id]
		if action is None:
			abort(404)

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
			return str(e)

		return response


	def get(self, item_id):
		action = state.get_action_manager()[item_id]
		action.notify()