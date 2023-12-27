from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# База даних користувачів
users = []

# База даних товарів
products = []


# Роут для додавання нових користувачів
@app.route("/add_user", methods=["POST"])
def add_user():
    user_data = request.get_json()
    users.append(user_data)
    return jsonify({"message": "User added successfully"})


# Роут для додавання нових товарів
@app.route("/add_product", methods=["POST"])
def add_product():
    product_data = request.get_json()
    products.append(product_data)
    return jsonify({"message": "Product added successfully"})


# Роут для видавання товарів за категорією
@app.route("/get_products_by_category", methods=["GET"])
def get_products_by_category():
    category = request.args.get("category")
    category_products = [product for product in products if product["category"] == category]
    return jsonify(category_products)


# Роут для оформлення замовлення
@app.route("/place_order", methods=["POST"])
def place_order():
    order_data = request.get_json()
    user = order_data["user"]
    selected_products = order_data["products"]

    # Перевірка наявності товарів та коштів у користувача
    for product in selected_products:
        if product not in products:
            return jsonify({"message": f"Product {product} not available"})
    if user["balance"] < sum(product["price"] for product in selected_products):
        return jsonify({"message": "Insufficient funds"})

    # Оновлення балансу та видалення товарів зі списку наявних
    user["balance"] -= sum(product["price"] for product in selected_products)
    for product in selected_products:
        products.remove(product)

    return jsonify({"message": "Order placed successfully"})


@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
