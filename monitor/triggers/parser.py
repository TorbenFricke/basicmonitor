import simpleeval, functools


default_values = {
	str: "",
	int: 0,
	float: 0,
}


def get_row(db, id, row_idx):
	return db.fetch_nth_reading(db.sensor_prefix + id, row_idx)[0]


def get_variable(path, sensor_manager):
	if not type(path == dict):
		TypeError("path is supposed to be a dict")
	if not len(path.keys()) == 3:
		ValueError("Cannot make sense of the variable path {}".format(path))
	for key in ["id", "row", "channel"]:
		if not key in path:
			raise TypeError("path must provide a {}".format(key))

	db = sensor_manager.db
	row = get_row(db, path["id"], path["row"])
	value = row[path["channel"]]

	if value is None:
		typ = sensor_manager[path["id"]].channels[path["channel"]]
		value = default_values[typ]

	return value


def evaluate(expression, variables, sensor_manager):
	def name_handler(node):
		path = variables[node.id]
		return get_variable(path, sensor_manager)

	val = simpleeval.simple_eval(expression, names=name_handler)

	return val



