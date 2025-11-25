from core.database.base_db import BaseDB

class Database(BaseDB):
    @BaseDB.db_operation
    def get_product_names_by_category(self, cur, category):

    @BaseDB.db_operation
    def get_product_price(self, cur, product):

    @BaseDB.db_operation
    def add_order(self, cur, order_data):

    @BaseDB.db_operation
    def get_all_orders(self, cur):

    @BaseDB.db_operation
    def delete_order(self, cur, order_id):

