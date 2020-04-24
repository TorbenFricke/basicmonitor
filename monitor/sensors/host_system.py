from monitor.sensors.base import Sensor
import psutil, time


class CPUPercentage(Sensor):
	channels = {"percentage": float}

	def fetch(self):
		return psutil.cpu_percent(interval=self.kwargs.get("psutil_interval", 0.5))


class RAMPercentage(Sensor):
	channels = {"percentage": float}

	def fetch(self):
		return psutil.virtual_memory()._asdict()["percent"]


class Uptime(Sensor):
	channels = {"seconds": float}

	def fetch(self):
		return time.time() - psutil.boot_time()



if __name__ == "__main__":
	print(f"CPU = {CPUPercentage().fetch()} %")
	print(f"RAM = {RAMPercentage().fetch()} %")
	print("Uptime = {:.1f} days".format(Uptime().fetch() / 60 / 60 / 24))

	print(Uptime().update())