import sqlite3
import datetime
import random
import os

class Database:
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    def _connect(self):
        return sqlite3.connect(self.db_path)

    @staticmethod
    def generate_order_id():
        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%d%H%M%S")
        r = random.randint(1000, 9999)
        return f"OD{ts}{r}"

    # =====================
    # GET: 商品名稱 (by category)
    # =====================
    def get_all_categories(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT category FROM commodity ORDER BY category")
            rows = cur.fetchall()
            return [row[0] for row in rows]
        
    def get_product_names_by_category(self, category):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT product FROM commodity WHERE category = ?", (category,))
            rows = cur.fetchall()
            return [row[0] for row in rows]

    # =====================
    # GET：商品價格
    # =====================
    def get_product_price(self, product):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT price 
                FROM commodity 
                WHERE product=?
            """, (product,))
            row = cur.fetchone()
            return row[0] if row else None

    # =====================
    # POST：新增訂單
    # =====================
    def add_order(self, order_data):
        with self._connect() as conn:
            cur = conn.cursor()
            order_id = self.generate_order_id()

            cur.execute("""
                INSERT INTO order_list
                (order_id, date, customer_name, product, amount, total, status, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                order_data["date"],           # 對應 date
                order_data["customer_name"],
                order_data["product"],        # 對應 product
                order_data["amount"],         # 對應 amount
                order_data["total"],          # 對應 total
                order_data["status"],
                order_data["note"]
            ))

            conn.commit()
            return order_id

    # =====================
    # GET：取得全部訂單（含商品價格）
    # =====================
    def get_all_orders(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    o.order_id,
                    o.date,
                    o.customer_name,
                    o.product,
                    c.price,
                    o.amount,
                    o.total,
                    o.status,
                    o.note
                FROM order_list o
                LEFT JOIN commodity c
                ON o.product = c.product
                ORDER BY o.date DESC
            """)
            rows = cur.fetchall()
            return [list(r) for r in rows]

    # =====================
    # DELETE：刪除訂單
    # =====================
    def delete_order(self, order_id):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM order_list 
                WHERE order_id=?
            """, (order_id,))
            conn.commit()
