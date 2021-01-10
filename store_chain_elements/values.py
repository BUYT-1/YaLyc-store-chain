from pathlib import Path


class DatabaseDoesntExist(Exception):
    pass


TABLES = {'available_item': ('id', 'item_id', 'shop_id', 'price_one', 'quantity'),
          'employee': ('id', 'name', 'shop_id', 'position_id', 'salary', 'other_info'),
          'item': ('id', 'name', 'supplier_id'),
          'position': ('id', 'name', 'description'),
          'shop': ('id', 'name'),
          'supplier': ('id', 'name'),
          'transaction': ('id', 'type', 'money_delta')}


HOME_DIR = str(Path.home())

STOCK_TR_TYPE = 1
SELL_TR_TYPE = 2
EARN_TR_TYPE = 3
SPEND_TR_TYPE = 4
