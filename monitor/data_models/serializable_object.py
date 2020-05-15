import json


class SerializableObject(object):
	_serialize_blacklist = ["update_handler"]
	"""Attributes of this object, that will not be serialized"""


	def to_dict(self):
		return {key: value for key, value in self.__dict__.items() if key not in self._serialize_blacklist}


	def to_json(self):
		return json.dumps(self.to_dict(), sort_keys=True)


	@classmethod
	def from_json(cls, js):
		d = json.loads(js)
		return cls(**d)

