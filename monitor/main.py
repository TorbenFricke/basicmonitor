from flask import Flask, render_template, send_from_directory
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def index():
	return react_app("index.html")


@app.route('/<path:path>')
def react_app(path):
	return send_from_directory('build', path)


from monitor.api.sensor import SensorDetailApi, SensorApi, SensorUpdateApi
from monitor.api.event import EventsApi
from monitor.api.trigger import TriggerApi, TriggerDetailApi, TriggerUpdateApi
from monitor.api.query import Query
from monitor.api.evaluate import Evaluate

# list sensors and add new ones
api.add_resource(SensorApi, '/sensors', '/sensors/')
api.add_resource(SensorDetailApi, '/sensors/<string:item_id>')
api.add_resource(SensorUpdateApi, '/sensors/<string:item_id>/update')
# triggers
api.add_resource(TriggerApi, '/triggers', '/triggers/')
api.add_resource(TriggerDetailApi, '/triggers/<string:item_id>')
api.add_resource(TriggerUpdateApi, '/triggers/<string:item_id>/update')
# events
api.add_resource(EventsApi, '/events')
# database queries
api.add_resource(Query, '/query/<string:sensor_id>')
# evaluate an expression, just as triggers do
api.add_resource(Evaluate, '/evaluate')


if __name__ == '__main__':
	app.run()
