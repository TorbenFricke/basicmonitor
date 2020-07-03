import requests, time

def push(message, api_token, user_key, device):
	return requests.post(
		"https://api.pushover.net/1/messages.json",
		data={
			"token": api_token,
			"user": user_key,
			"device": device,
			"message": message
		}
	)

from basicmonitor.actions import Action

class PushoverAction(Action):
	def __init__(self, **kwargs):
		# make sure the required API credentials are provided
		self.api_token = kwargs.pop("api_token")
		self.user_key = kwargs.pop("user_key")
		self.device = kwargs.pop("device")
		# initialize the superclass
		Action.__init__(self, **kwargs)


	def _notify(self, message):
		t = time.time()
		push(message, api_token=self.api_token, user_key=self.user_key, device=self.device)
		return "Send a push notification via Pushover. This took {:.1f} ms".format((time.time() - t) * 1000)