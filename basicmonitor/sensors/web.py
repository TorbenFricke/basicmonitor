from basicmonitor.sensors.base import Sensor
import requests, json


class HTML(Sensor):
	channels = {"content": str,
	            "elapsed": float,
	            "redirects": str,
	            "status_code": int,
	            "headers": str}


	def validate(self):
		# url was provided?
		if not "url" in self.__dict__:
			raise KeyError("HTML error needs 'url' argument")


	def fetch(self):
		data = {}
		try:
			req = requests.get(self.__dict__.get("url"))
		except Exception as e:
			return data
		data["content"] = req.text
		data["elapsed"] = req.elapsed.total_seconds()
		redirects = [h.url for h in req.history] + [req.url]
		try:
			redirects = redirects[1:]
		except:
			pass
		data["redirects"] = " ".join(redirects)
		data["status_code"] = req.status_code
		data["headers"] = json.dumps(dict(req.headers))

		return data



if __name__ == "__main__":
	sensor = HTML(url="s.torben.co")
	print(sensor.fetch())
	print(sensor.to_json())



