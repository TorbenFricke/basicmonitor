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

from monitor.api import SensorDetailApi, SensorApi, SensorUpdateApi, EventsApi

# list sensors and add new ones
api.add_resource(SensorApi, '/sensors', '/sensors/')
# show detail
api.add_resource(SensorDetailApi, '/sensors/<string:sensor_id>')
api.add_resource(SensorUpdateApi, '/sensors/<string:sensor_id>/update')
# events
api.add_resource(EventsApi, '/events')



if __name__ == '__main__':
	app.run()
