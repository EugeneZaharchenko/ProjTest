from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# База даних користувачів
users_list = [
    {'id': 1, 'name': 'Ньютон'},
    {'id': 2, 'name': 'Кюрі'},
    {'id': 3, 'name': 'Черчіль'}
]

# База даних товарів
products_list = [
    {'id': 1, 'name': 'телефон', 'price': 800},
    {'id': 2, 'name': 'рушниця', 'price': 6200},
    {'id': 3, 'name': 'їжа', 'price': 100},
    {'id': 3, 'name': 'набої', 'price': 50},
    {'id': 3, 'name': 'стартовий пакет Київстар', 'price': 0},
    {'id': 3, 'name': 'ноутбук', 'price': 40000}
]

goods = []


# Роут для додавання нових товарів
@app.route("/add_product", methods=["POST"])
def add_product():
    product_data = request.get_json()
    products_list.append(product_data)
    return jsonify({"message": "Product added successfully"})


# Роут для видавання товарів за категорією
@app.route("/get_products_by_category", methods=["GET"])
def get_products_by_category():
    category = request.args.get("category")
    category_products = [product for product in products_list if product["category"] == category]
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


@app.route("/main", methods=["GET"])
def main():
    return render_template("main.html")


@app.route("/users", methods=["GET"])
def users():
    return render_template("users.html", users=users_list)


# Роут для додавання нових користувачів
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form.get('user_name')
        new_user = {'id': len(users_list) + 1, 'name': new_user_name}
        users_list.append(new_user)
        return redirect(url_for('users'))


@app.route("/products", methods=["GET"])
def products():
    return render_template("products.html", products=products_list)


@app.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html", goods=goods)


if __name__ == "__main__":
    app.run(debug=True)
