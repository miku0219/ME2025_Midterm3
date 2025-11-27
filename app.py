from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        orders = db.get_all_orders()
        if request.args.get('warning'):
            warning = request.args.get('warning')
            return render_template('form.html', orders=orders, warning=warning)
        return render_template('form.html', orders=orders)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():

    # -------------------------
    #  GET：查詢（category / product）
    # -------------------------
    if request.method == 'GET':

        # 取得所有商品種類
        if request.args.get("all_categories") == "1":
            categories = db.get_all_categories()
            return jsonify({"categories": categories})

        # 依 category 查商品列表
        category = request.args.get('category')
        if category:
            products = db.get_product_names_by_category(category)
            return jsonify({"product": products})

        # 依 product 查價格
        product = request.args.get('product')
        if product:
            price = db.get_product_price(product)
            return jsonify({"price": price})

        return jsonify({"error": "請帶入 category 或 product 參數"}), 400


    # --------------------
    # POST
    # --------------------
    elif request.method == 'POST':
        data = request.get_json()

        order_data = {
            "date": data.get("date"),
            "customer_name": data.get("customer_name"),
            "product": data.get("product_name"),
            "amount": data.get("qty"),
            "total": data.get("subtotal"),
            "status": data.get("status"),
            "note": data.get("remark")
        }

        db.add_order(order_data)
        return jsonify({"message": "Order placed successfully"})

    # --------------------
    # DELETE
    # --------------------
    elif request.method == 'DELETE':
        oid = request.args.get("order_id")
        if not oid:
            return jsonify({"error": "order_id required"}), 400

        db.delete_order(oid)
        return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
