from .main import make_app
from . import actions
from . import api
from . import data_models
from . import sensors
from . import triggers

def run(prefix="", **kwargs):
	make_app(prefix=prefix).run(**kwargs)

