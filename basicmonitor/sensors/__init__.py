from basicmonitor.sensors.base import Sensor
from basicmonitor.sensors.host_system import *
from basicmonitor.sensors.web import *

sensors_available = list(Sensor.subclasses_by_name().keys())

from basicmonitor.sensors.manager import SensorManager
