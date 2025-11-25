import os
import sqlite3 as sql
from functools import wraps
import datetime
import random

class BaseDB:
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def db_operation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                with sql.connect(self.db_path) as db:
                    cur = db.cursor()
                    result = func(self, cur, *args, **kwargs)
                    db.commit()
                    return result
            except sql.Error as e:
                print(f"Database error in {func.__name__}: {e}")
            except Exception as e:
                print(f"Unexpected error in {func.__name__}: {e}")
            return None
        return wrapper

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"
