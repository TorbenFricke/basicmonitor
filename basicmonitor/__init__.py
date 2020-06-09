from .main import app
from . import actions
from . import api
from . import data_models
from . import sensors
from . import triggers

def run():
	app.run()