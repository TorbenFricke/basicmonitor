from monitor.helpers import uid
import json


class SerializableObject(object):
	_serialize_blacklist = ["update_handler"]
	"""Attributes of this object, that will not be serialized"""

	def __init__(self, **kwargs):
		# general info
		self.id = kwargs.pop("id", uid())
		self.name = kwargs.pop("name", "New Item")
		self.retain_for = kwargs.pop("retain_for", 90 * 24 * 60 * 60)
		self.enabled = kwargs.pop("enabled", True)

		# remember keyword arguments to be accessible by subclasses later. Compared to hard coding new attributes, this
		# has the advantage that the serialization stays the same.
		for key, value in kwargs.items():
			if not key in self.__dict__:
				self.__dict__[key] = value



	def to_dict(self):
		return {key: value for key, value in self.__dict__.items() if key not in self._serialize_blacklist}


	def to_json(self):
		return json.dumps(self.to_dict(), sort_keys=True)


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		return cls(**d)



class SubclassibleSerializableObject(SerializableObject):


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
