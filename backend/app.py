from flask import Flask, render_template, session, redirect, url_for, render_template, request, flash, jsonify
from database.db_connection import get_products,get_products_by_category, get_product_by_id
from database.data_processing import load_transactions, preprocess_data
from analysis.apriori_analysis import run_apriori
from database.db_connection import get_connection

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'your-secret-key'



@app.route('/')
def index():
    products = get_products()

    # Lấy danh sách danh mục duy nhất từ bảng Products
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Category FROM Products")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template('index.html', products=products, categories=categories)

@app.route('/recommendations')
def recommendations():
    # Tải và xử lý dữ liệu giao dịch
    transactions = load_transactions()
    transactions = preprocess_data(transactions)

    # Chạy thuật toán Apriori
    rules = run_apriori(transactions)

    # Chuyển đổi kết quả thành danh sách để hiển thị
    recommendations = []
    for _, rule in rules.iterrows():
        recommendations.append({
            'antecedents': list(rule['antecedents']),
            'consequents': list(rule['consequents']),
            'confidence': rule['confidence']
        })

    return render_template('recommendations.html', recommendations=recommendations)

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Tên đăng nhập không hợp lệ.")
    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Trả về sản phẩm theo danh mục dưới dạng JSON
@app.route('/api/products')
def api_products():
    category = request.args.get('category', 'All')
    if category == 'All':
        products = get_products()
    else:
        products = get_products_by_category(category)
    return jsonify(products)



# Chi tiết sản phẩm
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

# Thêm sản phẩm vào giỏ hàng
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash("Đã thêm vào giỏ hàng")
    return redirect(request.referrer or url_for('index'))

# Xem giỏ hàng
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    if not cart:
        return render_template('cart.html', items=[])

    conn = get_connection()
    cursor = conn.cursor()
    product_ids = list(map(int, cart.keys()))
    placeholders = ','.join(['?'] * len(product_ids))
    query = f"SELECT ProductID, ProductName, Price, ImagePath FROM Products WHERE ProductID IN ({placeholders})"
    cursor.execute(query, product_ids)
    products = cursor.fetchall()
    conn.close()

    items = []
    for product in products:
        pid = str(product[0])
        quantity = cart[pid]
        items.append((product[0], product[1], product[2], f"/static/{product[3]}", quantity))

    return render_template('cart.html', items=items)

# Cập nhật số lượng sản phẩm trong giỏ hàng
@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    action = request.form.get('action')
    cart = session.get('cart', {})

    if str(product_id) in cart:
        if action == 'add':
            cart[str(product_id)] += 1
        elif action == 'subtract':
            cart[str(product_id)] -= 1
            if cart[str(product_id)] <= 0:
                cart.pop(str(product_id))

    session['cart'] = cart
    return redirect(url_for('cart'))

# Xóa sản phẩm khỏi giỏ hàng
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash("Đã xóa sản phẩm khỏi giỏ")
    return redirect(url_for('cart'))

# Xóa toàn bộ giỏ hàng
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Đã xóa toàn bộ giỏ hàng")
    return redirect(url_for('cart'))



if __name__ == '__main__':
    app.run(debug=True, port=8000)



