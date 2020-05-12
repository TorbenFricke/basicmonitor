from flask_restful import Resource, request

from monitor import state


class Query(Resource):
	def get(self, sensor_id):
		db = state.get_db()
		table = db.sensor_prefix + sensor_id

		# get requested column, default to all
		try:
			assert "column" in request.args
			column = request.args.get("column")
			columns = ["time", column]
		except:
			columns = ["*"]

		# get requested row index, default to all
		try:
			row = int(request.args.get("row"))
		except:
			row = None


		if row is None:
			return db.fetch_columns(table, columns)
		else:
			return db.fetch_columns_nth(table, columns, row)
