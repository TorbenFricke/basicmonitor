import json

from flask import Response
from flask_restful import Resource

from basicmonitor import state


class EventsApi(Resource):
	def get(self):
		def events():
			for event in state.get_event_manager().subscribe():
				yield f"data: {event.get('message', 'no message')}\n\n{json.dumps(event, indent=2)}\n"

		return Response(
			events(),
			mimetype='text/event-stream'
		)