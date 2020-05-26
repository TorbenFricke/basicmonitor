from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort
import json

from monitor import validators

class DetailApi(Resource):
	def __init__(self, manager_provider, validation_mask):
		Resource.__init__(self)
		self.manager_provider = manager_provider
		"""A function that returns the relevent manager (i.e. SensorManager, TriggerManager, ...)"""
		self.validation_mask = validation_mask


	def get(self, item_id):
		item_manager = self.manager_provider()
		item = item_manager[item_id]
		if item is None:
			abort(404)

		data = item.to_dict()
		data["last_reading"] = item_manager.last_reading(item_id)
		return data


	def delete(self, item_id):
		self.manager_provider().delete(item_id)
		return "deleted {}".format(item_id)


	def put(self, item_id):
		item = self.manager_provider()[item_id]
		if item is None:
			abort(404)

		data = request.get_json(force=True)
		try:
			clean = validators.apply_validation_mask(data, self.validation_mask)
			for key, value in clean.items():
				if key in item.__dict__:
					setattr(item, key, value)

			# trigger event
			self.manager_provider().on_edit({"id": item.id})
			self.manager_provider().save(item.id)

		except Exception as e:
			return {"message": str(e)}

		return item.to_dict()


def do_nothing(*args): pass

class ListCreateApi(Resource):
	def __init__(self, manager_provider, validation_mask, item_class, on_item_created=do_nothing):
		Resource.__init__(self)
		self.manager_provider = manager_provider
		self.validation_mask = validation_mask
		self.item_class = item_class
		self.on_item_created = on_item_created


	def get(self):
		return [item.to_dict() for item in self.manager_provider().items]


	def post(self):
		data = request.get_json(force=True)

		try:
			clean = validators.apply_validation_mask(data, self.validation_mask)

			# make the item
			item = self.item_class.from_json(json.dumps(clean))

		except Exception as e:
			return {"message": str(e)}

		item_manager = self.manager_provider()
		item_manager.add(item)

		# do specific stuff in subclass
		self.on_item_created(item)

		return item.to_dict()