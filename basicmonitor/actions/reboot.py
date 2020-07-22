## before using this action you will likely have to enable rebooting without havig to enter the root password

# https://askubuntu.com/questions/168879/shutdown-from-terminal-without-entering-password

from basicmonitor.actions import Action
import os

class RebootAction(Action):
	def _notify(self, message):
		return os.system("shutown -r now")