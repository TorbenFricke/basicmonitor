from flask_restful import Resource, request

from basicmonitor import state
from basicmonitor.triggers import parser

class Evaluate(Resource):
	def post(self):
		data = request.get_json(force=True)

		try:
			out = {
				"message": parser.evaluate(
					expression=data["expression"],
		            variables=data["variables"],
		            sensor_manager=state.get_sensor_manager()),
				"error": False
			}
		except Exception as e:
			out = {
				"message": str(e),
				"error": True,
			}

		return out