import sqlite3 as sql
import os, threading, queue
from collections import defaultdict


def _dictify_select(f):
	def wrapped(*args, **kwargs):
		selection = f(*args, **kwargs)
		columns = [keys[0] for keys in selection.description]
		rows = selection.fetchall()
		return [
			{key: value for key, value in zip(columns, row)} for row in rows
		]
	return wrapped


def sanitize_characters(string, replace_invalid_with=""):
	for character in string:
		point = ord(character)

		if point == 0:
			yield replace_invalid_with
		elif 0xD800 <= point <= 0xDBFF:
			yield replace_invalid_with
		elif 0xDC00 <= point <= 0xDFFF:
			yield replace_invalid_with
		elif 0xFDD0 <= point <= 0xFDEF or (point % 0x10000) in (0xFFFE, 0xFFFF):
			yield replace_invalid_with
		else:
			yield character


def _scrub_table_name(identifier, replace_invalid_with=""):
	sanitized = "".join(sanitize_characters(identifier, replace_invalid_with))
	return '"' + sanitized.replace('"', "") + '"'


class Database(object):

	def __init__(self, path, **kwargs):
		self.echo = kwargs.pop("echo", False)
		self.path = path

		# general
		self.sensor_prefix = "sensor-"

		# make a db connection and corresponding lock
		self.connection = sql.connect(self.path, check_same_thread=False)
		self.lock = threading.Lock()


	def _log(self, msg):
		if self.echo:
			print('\033[94m' + msg + '\033[0m')


	def execute(self, sql, parameters=(), commit=False):
		self._log(sql)

		with self.lock:
			cursor = self.connection.cursor()
			if type(parameters) is list:
				ret = cursor.executemany(sql, parameters)
			else:
				ret = cursor.execute(sql, parameters)

			if commit:
				self.connection.commit()
				self._log("COMMIT")

		return ret


	def list_tables(self):
		rows = self.execute('SELECT name from sqlite_master where type="table"').fetchall()
		return [row[0] for row in rows]


	def columns(self, table_name):
		table_name = _scrub_table_name(table_name)
		rows = self.execute(
			"PRAGMA table_info({}); ".format(table_name)
		).fetchall()
		return [row[1] for row in rows]


	@_dictify_select
	def fetch_all(self, table_name):
		table_name = _scrub_table_name(table_name)
		return self.execute(
			"SELECT * from {}".format(table_name)
		)


	@_dictify_select
	def fetch_nth_reading(self, table_name, idx):
		table_name = _scrub_table_name(table_name)
		idx = int(idx)
		if idx > 0:
			return self.execute(
				"SELECT * from {} LIMIT 1 OFFSET {};".format(table_name, "time", idx)
			)
		else:
			idx = abs(idx) + 1
			return self.execute(
				"SELECT * from {} ORDER BY {} DESC LIMIT 1 OFFSET {};".format(table_name, "time", idx)
			)


	def fetch_last_reading(self, table_name):
		return self.fetch_nth_reading(table_name, -1)


	@_dictify_select
	def fetch_id(self, table_name, uid):
		table_name = _scrub_table_name(table_name)
		return self.execute(
			"SELECT * from {} where id=?".format(table_name),
			(uid, )
		)


	## Object related stuff
	def object_table(self, table_name):
		table_name = _scrub_table_name(table_name)
		self.execute(
			"CREATE TABLE IF NOT EXISTS {} (id text PRIMARY KEY, json text)".format(table_name),
		    commit=True
		)
		return table_name


	def save_object(self, table_name, obj):
		table_name = _scrub_table_name(table_name)
		self.execute(
			"REPLACE INTO {} VALUES(?, ?)".format(table_name),
			(obj.id, obj.to_json()),
			commit=True
		)


	def save_objects(self, table_name, objects):
		table_name = _scrub_table_name(table_name)
		# execute many is used instead of calling "save_object" multiple times. This is faster.
		self.execute(
			"REPLACE INTO {} VALUES(?, ?)".format(table_name),
			[(obj.id, obj.to_json()) for obj in objects],
			commit=True
		)


	def load_object(self, table_name, uid, factory_function):
		table_name = _scrub_table_name(table_name)
		result = self.fetch_id(table_name, uid)
		if not result:
			return
		result = result[0]

		obj = factory_function(result["json"])
		assert obj.id == result["id"]

		return obj



	def load_objects(self, table_name, factory_function):
		table_name = _scrub_table_name(table_name)
		results = self.fetch_all(table_name)

		objects = []
		for result in results:
			obj = factory_function(result["json"])
			assert obj.id == result["id"]

			objects.append(obj)

		return objects


	def delete_id(self, table_name, id, commit=True):
		table_name = _scrub_table_name(table_name)
		self.execute(
			"DELETE FROM {} where id=?".format(table_name),
			(id,),
			commit=commit
		)


	## channel related stuff
	def channel_table(self, sensor):
		# Creating the columns str is not safe against sql injection. Only use this function when safe!
		table_name = self.sensor_prefix + sensor.id
		table_name = _scrub_table_name(table_name)

		# TODO add compression support using https://docs.python.org/3/library/zlib.html
		# type conversions
		conversions = {
			float: "real",
			str: "text",
			int: "int",
		}

		columns = [
			"{} {}".format(key, conversions[typ]) for key, typ in sensor.channels.items()
		]
		columns = ["time real"] + columns
		columns_str = "(" + ", ".join(columns) + ")"

		self.execute(
			"CREATE TABLE IF NOT EXISTS {} {}".format(table_name, columns_str),
			commit=True
		)
		self.columns(table_name)
		return table_name


	def insert_reading(self, id, data):
		table_name = _scrub_table_name(self.sensor_prefix + id)
		columns = self.columns(table_name)

		d = defaultdict(None)
		d.update(data)
		parameters = tuple([d[key] for key in columns])

		para_str = ", ".join(["?"] * len(parameters))
		self.execute(
			"INSERT INTO {} VALUES({})".format(table_name, para_str),
			parameters,
			commit=True
		)


	def drop(self, table_name):
		table_name = _scrub_table_name(table_name)
		self.execute(
			"DROP TABLE IF EXISTS {}".format(table_name),
			commit=True
		)


	def remove_old_readings(self, table_name, older_than):
		table_name = _scrub_table_name(table_name)
		self.execute(
			"DELETE from {} where time < ?".format(table_name),
			(older_than, )
		)


if __name__ == "__main__":
	db = Database(":memory:", echo=True)
	db.object_table("sensors")
	db.object_table("cats")

	from monitor.sensors import Uptime, HTML

	db.save_object("sensors", Uptime())
	print(db.fetch_all("sensors"))

	sensor = HTML(url="http://google.com")
	db.channel_table(sensor)
	db.channel_table(sensor)
	db.channel_table(sensor)

	print(db.list_tables())