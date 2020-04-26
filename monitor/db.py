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


class DatabaseWorker(threading.Thread):
	def __init__(self, db):
		self.db = db
		threading.Thread.__init__(self)
		self.daemon = True


	def run(self):
		# establish connection now. This ensures the connection is only accessed by this thread, despite setting the
		# check_same_thread=False flag.
		connection = sql.connect(self.db.path, check_same_thread=False)
		while True:
			return_queue, args, kwargs = self.db.queue.get()
			try:
				return_queue.put(
					self.db.execute_with_connection(connection, *args, **kwargs)
				)
			except Exception as e:
				return_queue.put(e)
			finally:
				self.db.queue.task_done()


class Database(object):

	def __init__(self, path, **kwargs):
		self.echo = kwargs.pop("echo", False)
		self.path = path

		# general
		self.sensor_prefix = "sensor-"

		# make a single thread that interfaces with the database
		self.queue = queue.Queue()
		self.return_queues = defaultdict(queue.Queue)
		self.worker = DatabaseWorker(self)
		self.worker.start()


	def _log(self, msg):
		if self.echo:
			print('\033[94m' + msg + '\033[0m')


	def execute_with_connection(self, connection, sql, parameters=(), commit=False):
		self._log(sql)

		cursor = connection.cursor()
		if type(parameters) is list:
			ret = cursor.executemany(sql, parameters)
		else:
			ret = cursor.execute(sql, parameters)

		if commit:
			connection.commit()
			self._log("COMMIT")
		return ret


	def execute(self, *args, **kwargs):
		# unfortunately, we need have one return queue for every Thread.
		return_queue = self.return_queues[threading.get_ident()]
		self.queue.put((return_queue, args, kwargs))
		ret = return_queue.get()
		if isinstance(ret, Exception):
			raise ret
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
	def fetch_last_reading(self, table_name, column="time"):
		table_name = _scrub_table_name(table_name)
		return self.execute(
			"SELECT * from {} ORDER BY {} DESC LIMIT 1;".format(table_name, column)
		)


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