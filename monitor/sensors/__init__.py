from monitor.sensors.base import Sensor
from monitor.sensors.host_system import *
from monitor.sensors.web import *

sensors_available = list(Sensor.subclasses_by_name().keys())

from monitor.sensors.manager import SensorManager
