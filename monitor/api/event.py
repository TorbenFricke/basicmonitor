import json

from flask import Response
from flask_restful import Resource

from monitor import state


class EventsApi(Resource):
	def get(self):
		def events():
			for event in state.get_event_manager().subscribe():
				yield json.dumps(event, indent=2) + "\n"

		return Response(
			events(),
			mimetype='application/json'
		)