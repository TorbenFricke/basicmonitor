from flask import Flask, send_from_directory, Blueprint
from flask_restful import Api


def make_app(prefix=""):
	# clean up prefix (if a prefix was provided)
	if prefix != "":
		prefix = "/" + prefix.strip(" /")

	if not type(prefix) == str: raise TypeError("Prefix needs to be a string")

	bp = Blueprint('basicmonitor', __name__)

	@bp.route('/')
	def index():
		return react_app("index.html")


	@bp.route('/<path:path>')
	def react_app(path):
		return send_from_directory('build', path)


	from basicmonitor.api.sensor import SensorDetailApi, SensorApi, SensorUpdateApi
	from basicmonitor.api.event import EventsApi
	from basicmonitor.api.trigger import TriggerApi, TriggerDetailApi, TriggerUpdateApi
	from basicmonitor.api.action import ActionApi, ActionDetailApi, ActionNotifyApi
	from basicmonitor.api.query import Query
	from basicmonitor.api.evaluate import Evaluate

	api = Api(bp)

	# list sensors and add new ones
	api.add_resource(SensorApi, '/sensors', '/sensors/')
	api.add_resource(SensorDetailApi, '/sensors/<string:item_id>')
	api.add_resource(SensorUpdateApi, '/sensors/<string:item_id>/update')
	# triggers
	api.add_resource(TriggerApi, '/triggers', '/triggers/')
	api.add_resource(TriggerDetailApi, '/triggers/<string:item_id>')
	api.add_resource(TriggerUpdateApi, '/triggers/<string:item_id>/update')
	# actions
	api.add_resource(ActionApi, '/actions', '/actions/')
	api.add_resource(ActionDetailApi, '/actions/<string:item_id>')
	api.add_resource(ActionNotifyApi, '/actions/<string:item_id>/update', '/actions/<string:item_id>/send')
	# events
	api.add_resource(EventsApi, '/events')
	# database queries
	api.add_resource(Query, '/query/<string:sensor_id>')
	# evaluate an expression, just as triggers do
	api.add_resource(Evaluate, '/evaluate')


	# make sure we do not serve a staic folder. This could interfere with our Webapp depending on the url prefix.
	app = Flask(__name__, static_url_path=None, static_folder=None)
	app.register_blueprint(bp, url_prefix=prefix)

	# allow CORS in Debug mode
	if app.debug:
		from flask_cors import CORS
		CORS(app)
		print("Cross-Origin Resource Sharing (CORS) was enabled for debug mode")

	from flask_compress import Compress
	Compress(app)

	return app


if __name__ == '__main__':
	make_app().run()
