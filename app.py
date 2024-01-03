from flask import Flask, request, render_template, redirect, url_for, abort, make_response

app = Flask(__name__)

# База даних користувачів
users_list = [
    {'id': 1, 'name': 'Ньютон'},
    {'id': 2, 'name': 'Кюрі'},
    {'id': 3, 'name': 'Черчіль'}
]

# База даних товарів
categories = ['Всі', 'Електроніка', 'Їжа', 'Необхідне']

products_list = {
    'Електроніка': [{'name': 'телефон', 'price': 800},
                    {'name': 'стартовий пакет Київстар', 'price': 0},
                    {'name': 'ноутбук', 'price': 40000}
                    ],
    'Їжа': [{'name': 'шоколад', 'price': 100},
            {'name': 'вода', 'price': 10},
            {'name': 'сир', 'price': 150}
            ],
    'Необхідне': [{'name': 'рушниця', 'price': 6200},
                  {'name': 'набої', 'price': 50}]

}

goods_to_buy = []


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
    _products = [product for products in products_list.values() for product in products]
    return render_template("products.html", products=_products, categories=categories)


# Роут для видавання товарів за категорією
@app.route("/get_products_by_category", methods=["GET"])
def get_products_by_category():
    category = request.args.get("get_category") or 'Всі'
    if category == 'Всі':
        _products = [product for products in products_list.values() for product in products]
        return render_template("products.html", products=_products, categories=categories)
    else:
        category_products = [product for product in products_list.get(category)]
        return render_template('products.html', categories=categories, products=category_products)


# Роут для додавання нових товарів
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        category = request.form.get('category')
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')

        # Add the product to the specified category
        products_list[category].append({'name': product_name, 'price': product_price})

        return redirect(url_for('products'))
    get_products_by_category()
    return render_template("cart.html", goods_to_buy=goods_to_buy)


# Роут для оформлення замовлення
@app.route("/place_order", methods=["POST"])
def place_order():
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')
        total_price = 0

        # Retrieve selected items and calculate the total price
        selected_products = []
        for item in selected_items:
            product_name, product_price = item.split('_')
            product_price = int(product_price)
            selected_product = {'name': product_name, 'price': product_price}
            total_price += product_price
            selected_products.append(selected_product)

        # Add the selected items to the goods list
        goods_to_buy.extend(selected_products)

        response = make_response(
            render_template("cart.html", selected_products=selected_products, total_price=total_price))

        return response

    abort(400, "Bad Request: Only POST requests are allowed for this endpoint")


@app.route("/make_order", methods=["POST"])
def make_order():
    if request.method == 'POST':
        print('Замовлення сформоване')

        return redirect(url_for('products'))

    abort(400, "Bad Request: Only POST requests are allowed for this endpoint")


if __name__ == "__main__":
    app.run(debug=True)
