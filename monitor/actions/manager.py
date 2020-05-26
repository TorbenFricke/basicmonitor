from monitor.actions.base import Action
from monitor.data_models import ItemManager


class ActionManager(ItemManager):
	def __init__(self, db):
		ItemManager.__init__(self,
			db=db,
			item_factory_function=Action.from_json,
			item_table_name="actions",
		    item_name="action",
			reading_table_prefix="action-"
		)