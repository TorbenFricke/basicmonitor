from unittest import TestCase
from monitor.sensors.manager import SensorManager
from monitor.sensors import HTML, Uptime
from monitor.db import Database


def update(db, s):
	n_rows_before = len(db.fetch_all(db.sensor_prefix + s.id))
	s.update()
	rows = db.fetch_all(db.sensor_prefix + s.id)
	assert len(rows) - n_rows_before == 1
	assert rows[-1]["seconds"] > 0

	s.update()
	rows = db.fetch_all(db.sensor_prefix + s.id)
	assert len(rows) - n_rows_before == 2
	assert rows[-1]["seconds"] > rows[-2]["seconds"]


def add(manager, sensor):
	manager.add(sensor)
	return sensor.id


def test_context(f):
	def wrapped(self):
		db = Database(":memory:", echo=True)
		manager = SensorManager(db)
		return f(self, db, manager)
	return wrapped


class SensorManagerTest(TestCase):

	@test_context
	def test_save_load(self, db, manager):
		s = HTML(url="http://google.com")
		# also saves the new sensor to the DB
		manager.add(s)
		manager.load()
		assert len(manager.sensors) == 1
		assert manager[s.id].to_json() == s.to_json()


	@test_context
	def test_update(self, db, manager):
		s = Uptime()
		s.update()
		manager.add(s)

		rows = db.fetch_all(db.sensor_prefix + s.id)
		assert len(rows) == 0

		update(db, s)


	@test_context
	def test_update_after_load(self, db, manager):
		s = Uptime()
		manager.add(s)

		update(db, s)
		assert len(db.fetch_all(db.sensor_prefix + s.id)) == 2

		manager.load()
		update(db, s)

		assert len(db.fetch_all(db.sensor_prefix + s.id)) == 4


	@test_context
	def test_delete(self, db, manager):
		id1 = add(manager, Uptime())
		# add one sensor twice (should not add a duplicate)
		s = Uptime()
		add(manager, s)
		id2 = add(manager, s)
		id3 = add(manager, Uptime())

		assert len(manager.sensors) == 3

		manager.delete(id2)

		assert len(manager.sensors) == 2
		assert manager[id1].id == id1
		assert manager[id2] is None
		assert manager[id3].id == id3


	@test_context
	def test_remnants(self, db, manager):
		id = add(manager, Uptime())

		# table exits?
		assert any([id in tab_name for tab_name in db.list_tables()])

		manager.delete(id)

		# table gone?
		assert not any([id in tab_name for tab_name in db.list_tables()])

		rows = db.fetch_all("sensors")
		for row_id, js in rows:
			assert id != row_id

