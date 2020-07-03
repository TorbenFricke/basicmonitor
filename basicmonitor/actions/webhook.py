from basicmonitor.actions import Action
import requests

allowed_methods = ["get", "post", "put", "delete"]

class WebhookAction(Action):
	def __init__(self, **kwargs):
		# make sure the required info is provided
		self.url = kwargs.pop("url")
		self.method = kwargs.pop("method")
		# valudate method
		if not self.method in allowed_methods:
			raise ValueError(f"method {self.method} not allowd")
		# initialize the superclass
		Action.__init__(self, **kwargs)


	def _notify(self, message):
		req = requests.request(
			method=self.method,
			url=self.url,
			data={"message": message}
		)
		return f"Made a {self.method.upper()} request to {self.url}. Status code {req.status_code}. " \
		       f"This took {req.elapsed:.1f} ms"