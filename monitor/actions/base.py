from monitor.data_models import SubclassibleSerializableObject
import time


def do_nothing(*args): pass


class Action(SubclassibleSerializableObject):
	channels = {"message": bool}

	def __init__(self, **kwargs):
		self.update_handler = do_nothing

		self.cooldown = kwargs.pop("cooldown", 60)
		"""how long, between two messages"""
		self.last_notify = kwargs.pop("last_notify", -1)

		SubclassibleSerializableObject.__init__(self, **kwargs)


	def notify(self, message):
		now = time.time()
		time_until_cooldown = self.last_notify + self.cooldown - now
		# skip if still in cooldown
		if time_until_cooldown > 0:
			return f"in cooldown for {time_until_cooldown} more seconds"

		# cause the actual notification
		response = self._notify(message)

		# call the update handler - used to write to Database
		self.update_handler(self.id, message)

		self.last_notify = now

		return response


	# override me
	def _notify(self, message):
		print(message)
		return "print to std output"


class DebugAction(Action):
	pass