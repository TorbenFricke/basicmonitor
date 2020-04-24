import json
from monitor.sensors import sensors_available, Sensor


class SensorManager(object):
	def __init__(self, db):
		self.sensors = []
		self.db = db
		self.sensors_table = db.object_table("sensors")


	def add(self, sensor):
		# overwrite old sensor with same UID
		for s in self.sensors:
			if sensor.id == s.id:
				self.delete(s.id)
		# append new sensor
		self.sensors.append(sensor)
		self.link_sensor(sensor)

		self.save()


	def link_sensor(self, sensor):
		# make and link corresponding DB table
		self.db.channel_table(sensor)
		sensor.update_handler = self.db.insert_reading


	def delete(self, uid):
		for i, s in enumerate(self.sensors):
			if not s.id == uid:
				continue
			# found the sensor
			del self.sensors[i]
			# remove corresponding DB table
			self.db.delete_id(self.sensors_table, uid)
			self.db.drop(self.db.sensor_prefix + uid)

			return True
		return False


	def last_reading(self, uid):
		return self.db.fetch_all(self.db.sensor_prefix + uid)[-1]


	def save(self):
		self.db.save_objects(self.sensors_table, self.sensors)


	def load(self):
		self.sensors = self.db.load_objects(self.sensors_table, Sensor.from_json)
		for sensor in self.sensors:
			self.link_sensor(sensor)


	def __getitem__(self, uid):
		for s in self.sensors:
			if uid == s.id:
				return s