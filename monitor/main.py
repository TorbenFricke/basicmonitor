from flask import Flask, render_template, send_from_directory
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
	return render_template("app.html")


from monitor.api import SensorDetailApi, SensorApi, DebugAddSensor

# list sensors and add new ones
api.add_resource(SensorApi, '/sensors', '/sensors/')
api.add_resource(DebugAddSensor, '/debug')
# show detail
api.add_resource(SensorDetailApi, '/sensors/<string:sensor_id>')



if __name__ == '__main__':
	app.run()
