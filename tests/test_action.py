from unittest import TestCase
from basicmonitor.actions import Action

class SensorManagerTest(TestCase):

	def test_seraialize(self):
		action = Action()
		d = action.to_dict()
		assert "time_to_next_action" not in d