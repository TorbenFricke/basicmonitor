from basicmonitor.actions.base import Action
from basicmonitor.data_models import ItemManager
from basicmonitor.data_models import UpdateWorker


class ActionManager(ItemManager):
	def __init__(self, db):
		ItemManager.__init__(self,
			db=db,
			item_factory_function=Action.from_json,
			item_table_name="actions",
		    item_name="action",
			reading_table_prefix="action-"
		)

		self.worker = UpdateWorker(
			self,
			time_to_update_function=lambda item: item.time_to_next_action,
			update_function=lambda item: item.notify(),
		)
		self.worker.start()