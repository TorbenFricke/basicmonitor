from monitor.actions.base import Action
from monitor.actions.pushover import PushoverAction
from monitor.actions.manager import ActionManager

actions_available = list(Action.subclasses_by_name().keys())