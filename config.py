import os

from RPA.Robocorp.WorkItems import WorkItems


class RCCWortItems:

    def __init__(self):
        if os.getenv('ENVIRONMENT') == 'PROD':
            work_items = WorkItems()
            work_items.get_input_work_item()
            work_item = work_items.get_work_item_payload()
            self.search_phrase = work_item["search_phrase"]
            self.no_of_months = work_item.get("no_of_months", 1)
            self.category = work_item.get("category")
        else:
            self.search_phrase = "ICC"
            self.no_of_months = 1
            self.category = "Stories"
