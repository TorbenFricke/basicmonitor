from monitor.helpers import uid
from monitor.dataModels import SerializableObject
import json, time


def do_nothing(*args): pass


class Sensor(SerializableObject):
	channels = {}
	"""provide Channel information in subclasses. Must be overwritten in subclasses"""

	_serialize_blacklist = ["update_handler"]

	def __init__(self, name="sensor", interval=5*60, **kwargs):
		# was the channel information provided?
		if not self.channels:
			raise KeyError("No channel data was provided for this sensor. This needs to be done when subclassing.")

		# general information
		self.name = name
		self.id = kwargs.pop("id", uid())
		assert type(self.id) is str
		self.interval = interval
		self.retain_for = kwargs.pop("retain_for", 90*24*60*60)
		self.enabled = kwargs.pop("enabled", True)

		# keep track of the last update
		self.last_update = kwargs.pop("last_update", -1)

		# update handler function
		self.update_handler = do_nothing

		# remember keyword arguments to be accessible by subclasses later. Compared to hard coding new attributes, this
		# has the advantage that the serialization stays the same.
		for key, value in kwargs.items():
			if not key in self.__dict__:
				self.__dict__[key] = value

		# run validation handled by subclass
		self.validate()


	def to_dict(self):
		attributes = SerializableObject.to_dict(self)
		# also save the type (ie. subclass)
		attributes["type"] = str(self.__class__.__name__)
		return attributes


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		subclasses = cls.subclasses_by_name()

		# is that subclass known?
		if not d["type"] in subclasses:
			raise KeyError("Sensor cannot be loaded. Sensor of type {} not found.".format(d["type"]))
		subclass = subclasses[d["type"]]

		# remove stuff we do not want to show up in the kwargs of the loaded object
		d.pop("type")
		d.update(d.pop("kwargs", {}))
		return subclass(**d)


	@classmethod
	def subclasses_by_name(cls):
		return {s.__name__: s for s in cls.__subclasses__()}


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
