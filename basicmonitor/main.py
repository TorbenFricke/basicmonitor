from flask import Flask, render_template, send_from_directory
from flask_restful import Api
#from flask_compress import Compress
from flask_cors import CORS

app = Flask(__name__, template_folder="build")
CORS(app)
#Compress(app)
api = Api(app)


prefix = "/subdir2"

@app.route(f'{prefix}')
@app.route(f'{prefix}/')
@app.route(f'{prefix}/index.html')
def index():
	return render_template("index.html", prefix=prefix)


@app.route(f'{prefix}/<path:path>')
def react_app(path):
	return send_from_directory('build', path)


from basicmonitor.api.sensor import SensorDetailApi, SensorApi, SensorUpdateApi
from basicmonitor.api.event import EventsApi
from basicmonitor.api.trigger import TriggerApi, TriggerDetailApi, TriggerUpdateApi
from basicmonitor.api.action import ActionApi, ActionDetailApi, ActionNotifyApi
from basicmonitor.api.query import Query
from basicmonitor.api.evaluate import Evaluate

# list sensors and add new ones
api.add_resource(SensorApi, f'{prefix}/sensors', f'{prefix}/sensors/')
api.add_resource(SensorDetailApi, f'{prefix}/sensors/<string:item_id>')
api.add_resource(SensorUpdateApi, f'{prefix}/sensors/<string:item_id>/update')
# triggers
api.add_resource(TriggerApi, f'{prefix}/triggers', f'{prefix}/triggers/')
api.add_resource(TriggerDetailApi, f'{prefix}/triggers/<string:item_id>')
api.add_resource(TriggerUpdateApi, f'{prefix}/triggers/<string:item_id>/update')
# actions
api.add_resource(ActionApi, f'{prefix}/actions', f'{prefix}/actions/')
api.add_resource(ActionDetailApi, f'{prefix}/actions/<string:item_id>')
api.add_resource(ActionNotifyApi, f'{prefix}/actions/<string:item_id>/update')
# events
api.add_resource(EventsApi, f'{prefix}/events')
# database queries
api.add_resource(Query, f'{prefix}/query/<string:sensor_id>')
# evaluate an expression, just as triggers do
api.add_resource(Evaluate, f'{prefix}/evaluate')


if __name__ == '__main__':
	app.run()
