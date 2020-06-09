from basicmonitor.helpers import uid
from basicmonitor.data_models import SubclassibleItem
import json, time


def do_nothing(*args): pass


class Sensor(SubclassibleItem):
	channels = {}
	"""provide Channel information in subclasses. Must be overwritten in subclasses"""

	def __init__(self, interval=5*60, **kwargs):
		# was the channel information provided?
		if not self.channels:
			raise KeyError("No channel data was provided for this sensor. This needs to be done when subclassing.")

		# general information
		self.interval = interval

		SubclassibleItem.__init__(self, **kwargs)

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# update handler function
		self.update_handler = do_nothing


		SubclassibleItem.__init__(self, **kwargs)

		# run validation handled by subclass
		self.validate()


	def update(self):
		t = time.time()
		self.last_update = t
		fetched = self.fetch()

		# convert to dict, if only one value is expected
		if len(self.channels) == 1 and not isinstance(fetched, dict):
			fetched = {list(self.channels.keys())[0]: fetched}

		if not isinstance(fetched, dict):
			raise TypeError(
				"A sensor returned an unknown type in its fetch() call. fetch() sould return a str, float or dict")

		reading = {
			"time": t
		}
		for key in self.channels:
			if not key in fetched:
				reading[key] = None
			else:
				reading[key] = fetched[key]

		# call the update handler - used to write to Database
		self.update_handler(self.id, reading)

		return reading


	# override me (optional)
	def validate(self):
		pass


	# override me
	def fetch(self):
		"""
		Fetches a new sensor reading. To be override by subclass.

		:return:
		"""
		raise NotImplementedError
