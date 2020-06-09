from monitor.data_models import SubclassibleItem
import time


def do_nothing(*args): pass


class Action(SubclassibleItem):
	channels = {"message": str, "response": str}

	def __init__(self, **kwargs):
		self.update_handler = do_nothing

		self.cooldown = kwargs.pop("cooldown", 60)
		"""how long, between two messages"""
		self.last_notify = kwargs.pop("last_notify", -1)

		self.queued_messages = kwargs.pop("queued_messages", [])

		SubclassibleItem.__init__(self, **kwargs)


	def assemble_message(self, message=None):
		_message = ""

		if type(message) is None and len(self.queued_messages) == 0:
			# No message to build
			return None

		if not type(message) is None:
			_message += message

		# assemble message including queue
		if len(self.queued_messages) > 1:
			_message += "\nQueued Messages:\n"
			_message += "\n".join(map(str, self.queued_messages))
		self.queued_messages = []

		return _message


	def notify(self, message=None, force_send=False):
		now = time.time()
		time_until_cooldown = self.last_notify + self.cooldown - now
		# skip if still in cooldown
		if time_until_cooldown > 0 and not force_send:
			if type(message) is None:
				return "No message to be queued"

			self.queued_messages.append(message)
			# send an update to the UI - no database entry is created; the message is instead queued
			self.update_handler(self.id)
			return f"in cooldown for {time_until_cooldown} more seconds"

		# assemble message
		message = self.assemble_message(message)
		if type(message) is None:
			return "No message to be send"

		# cause the actual notification
		response = self._notify(message)

		# call the update handler - used to write to Database
		self.update_handler(self.id, {
			"time": now,
			"message": message,
			"response": str(response),
		})

		self.last_notify = now

		return response


	# override me
	def _notify(self, message):
		print(message)
		return "print to std output"


class DebugAction(Action):
	pass