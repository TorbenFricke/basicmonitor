from basicmonitor.actions.base import Action, DebugAction
from basicmonitor.actions.manager import ActionManager
from basicmonitor.actions.pushover import PushoverAction
from basicmonitor.actions.webhook import WebhookAction


actions_available = list(Action.subclasses_by_name().keys())