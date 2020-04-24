from unittest import TestCase
import random, threading, queue, time
from uuid import uuid4
from monitor.db import Database
from monitor.sensors import HTML, CPUPercentage, Sensor

# make test Database
db = Database(":memory:", echo=False)


def make_sensors():
	"""makes two dummy sensors"""
	return [HTML(url="http://google.com"), CPUPercentage()]


class DBTest(TestCase):

	def test_write(self):
		table_name = db.object_table("test_write")

		self.assertEqual(len(db.columns(table_name)), 2)

		db.save_object(table_name, HTML(url="http://google.com"))
		db.save_object(table_name, CPUPercentage())


	def test_write_read(self):
		sensors = make_sensors()
		table = db.object_table("test_write_read")

		db.save_objects(table, sensors)
		new_sensors = db.load_objects(table, Sensor.from_json)

		self.assertEqual(len(sensors), len(new_sensors))
		for old, new in zip(sensors, new_sensors):
			self.assertEqual(old.to_json(), new.to_json())


	def test_delete(self):
		sensors = make_sensors()
		table_name = db.object_table("test_delete")

		db.save_objects(table_name, sensors)
		db.delete_id(table_name, sensors[1].id)
		new_sensors = db.load_objects(table_name, Sensor.from_json)

		self.assertEqual(len(sensors) - 1, len(new_sensors))
		self.assertEqual(sensors[0].to_json(), new_sensors[0].to_json())


	def test_make_channel_table(self):
		sensor = HTML(url="http://google.com")
		table_name = db.channel_table(sensor)
		assert "elapsed" in db.columns(table_name)
		db.drop(table_name)


	def test_save_data_channel_table(self):
		sensor = HTML(url="http://google.com")
		table_name = db.channel_table(sensor)
		data = []
		for i in range(3):
			data.append(sensor.update())
			db.insert_reading(sensor.id, data[-1])
		new_data = db.fetch_all(table_name)
		for old, new in zip(data, new_data):
			for key, old_value in old.items():
				self.assertEqual(old_value, new[key])
		# do some tests
		db.drop(table_name)


	def test_create_table_twice(self):
		table = db.object_table("test_create_table_twice")
		db.save_object(table, CPUPercentage())
		# check to see if we overwrite old table
		table = db.object_table("test_create_table_twice")
		obj = db.load_objects(table, Sensor.from_json)[0]
		assert obj.interval >= 0


	def test_db_traffic(self):
		available = list(Sensor.subclasses_by_name().values())
		table_name = db.object_table("test_db_traffic")
		error_queue = queue.Queue()

		def random_object():
			return random.choice(available)(
				url=str(uuid4()),
				name=str(uuid4()),
				interval=random.random(),
			)

		def write_read_delete():
			sensors = {}
			for i in range(80):
				sensor = random_object()
				sensors[sensor.id] = sensor.to_json()
				db.save_object(table_name, sensor)

				# in 50% of cases, read an object and compare it to an old one
				if random.choice([True, False]):
					old_id = random.choice(list(sensors.keys()))
					new = db.load_object(table_name, old_id, Sensor.from_json)
					assert sensors[old_id] == new.to_json()

				# in 50% of cases, delete an object and check if its gone
				if random.choice([True, False]):
					old_id = random.choice(list(sensors.keys()))
					del sensors[old_id]
					db.delete_id(table_name, old_id)
					assert db.load_object(table_name, old_id, Sensor.from_json) is None

		def test_func():
			try:
				write_read_delete()
			except Exception as e:
				error_queue.put(e)

		threads = []
		for i in range(100):
			t = threading.Thread(target=test_func)
			t.start()
			threads.append(t)

		while any([t.is_alive() for t in threads]):
			time.sleep(0.1)

		# raise any errors in main thread
		try:
			raise error_queue.get_nowait()
		except queue.Empty:
			pass
