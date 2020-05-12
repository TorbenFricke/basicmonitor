from flask_restful import Resource, request

from monitor import state
from monitor.triggers import parser

class Evaluate(Resource):
	def post(self):
		data = request.get_json(force=True)

		try:
			out = {
				"message": parser.evaluate(
					expression=data["expression"],
		            variables=data["variables"],
		            sensor_manager=state.get_sensor_manager()),
				"worked": True
			}
		except Exception as e:
			out = {
				"message": str(e),
				"worked": True,
			}

		return out