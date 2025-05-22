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
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MaTaiKhoan FROM TaiKhoan WHERE TenDangNhap = ? AND MatKhau = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            session['username'] = username
            session['ma_tai_khoan'] = result[0]
            flash("Đăng nhập thành công!")
            return redirect(url_for('index'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng!")
            return redirect(url_for('login'))

    return render_template('login.html')


# Đăng xuất
@app.route('/logout')
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.")
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
    if 'ma_tai_khoan' in session:
        ma_tai_khoan = session['ma_tai_khoan']
        conn = get_connection()
        cursor = conn.cursor()

        # Kiểm tra nếu sản phẩm đã có trong giỏ thì cập nhật số lượng
        cursor.execute("SELECT SoLuong FROM GioHang WHERE MaTaiKhoan = ? AND ProductID = ?", (ma_tai_khoan, product_id))
        existing = cursor.fetchone()

        if existing:
            new_qty = existing[0] + 1
            cursor.execute("UPDATE GioHang SET SoLuong = ?, NgayThem = GETDATE() WHERE MaTaiKhoan = ? AND ProductID = ?",
                           (new_qty, ma_tai_khoan, product_id))
        else:
            cursor.execute("INSERT INTO GioHang (MaTaiKhoan, ProductID, SoLuong) VALUES (?, ?, 1)", (ma_tai_khoan, product_id))

        conn.commit()
        conn.close()
    else:
        # Lưu vào session nếu chưa đăng nhập
        cart = session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        session['cart'] = cart

    flash("Đã thêm vào giỏ hàng")
    return redirect(request.referrer or url_for('cart'))


# Xem giỏ hàng
@app.route('/cart')
def cart():
    if 'ma_tai_khoan' in session:
        ma_tai_khoan = session['ma_tai_khoan']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.ProductID, p.ProductName, p.Price, p.ImagePath, g.SoLuong
            FROM GioHang g
            JOIN Products p ON g.ProductID = p.ProductID
            WHERE g.MaTaiKhoan = ?
        """, (ma_tai_khoan,))
        items = cursor.fetchall()
        conn.close()
        items = [(item[0], item[1], item[2], f"/static/{item[3]}", item[4]) for item in items]
    else:
        cart = session.get('cart', {})
        if not cart:
            return render_template('cart.html', items=[])
        conn = get_connection()
        cursor = conn.cursor()
        product_ids = list(map(int, cart.keys()))
        placeholders = ','.join(['?'] * len(product_ids))
        cursor.execute(f"SELECT ProductID, ProductName, Price, ImagePath FROM Products WHERE ProductID IN ({placeholders})", product_ids)
        products = cursor.fetchall()
        conn.close()
        items = [(p[0], p[1], p[2], f"/static/{p[3]}", cart[str(p[0])]) for p in products]

    return render_template('cart.html', items=items)


# Cập nhật số lượng sản phẩm trong giỏ hàng
@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    action = request.form.get('action')
    
    if 'ma_tai_khoan' in session:
        ma_tai_khoan = session['ma_tai_khoan']
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SoLuong FROM GioHang WHERE MaTaiKhoan = ? AND ProductID = ?", (ma_tai_khoan, product_id))
        row = cursor.fetchone()

        if row:
            new_qty = row[0] + 1 if action == 'add' else row[0] - 1
            if new_qty <= 0:
                cursor.execute("DELETE FROM GioHang WHERE MaTaiKhoan = ? AND ProductID = ?", (ma_tai_khoan, product_id))
            else:
                cursor.execute("UPDATE GioHang SET SoLuong = ?, NgayThem = GETDATE() WHERE MaTaiKhoan = ? AND ProductID = ?", (new_qty, ma_tai_khoan, product_id))
            conn.commit()
        conn.close()

    else:
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
    if 'ma_tai_khoan' in session:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GioHang WHERE MaTaiKhoan = ? AND ProductID = ?", (session['ma_tai_khoan'], product_id))
        conn.commit()
        conn.close()
    else:
        cart = session.get('cart', {})
        cart.pop(str(product_id), None)
        session['cart'] = cart
    flash("Đã xóa sản phẩm khỏi giỏ hàng")
    return redirect(url_for('cart'))


# Xóa toàn bộ giỏ hàng
@app.route('/clear_cart')
def clear_cart():
    if 'ma_tai_khoan' in session:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GioHang WHERE MaTaiKhoan = ?", (session['ma_tai_khoan'],))
        conn.commit()
        conn.close()
    else:
        session.pop('cart', None)
    flash("Đã xóa toàn bộ giỏ hàng")
    return redirect(url_for('cart'))

# Thanh toán
@app.route('/checkout')
def checkout():
    if 'ma_tai_khoan' not in session:
        flash("Vui lòng đăng nhập để thanh toán.")
        return redirect(url_for('login'))

    ma_tai_khoan = session['ma_tai_khoan']
    conn = get_connection()
    cursor = conn.cursor()

    # Lấy thông tin người dùng
    cursor.execute("SELECT MaNguoiDung FROM NguoiDung WHERE MaTaiKhoan = ?", (ma_tai_khoan,))
    nguoidung = cursor.fetchone()
    if not nguoidung:
        flash("Không tìm thấy thông tin người dùng.")
        return redirect(url_for('cart'))

    ma_nguoidung = nguoidung[0]

    # Lấy giỏ hàng từ DB
    cursor.execute("""
        SELECT g.ProductID, p.Price, g.SoLuong
        FROM GioHang g
        JOIN Products p ON g.ProductID = p.ProductID
        WHERE g.MaTaiKhoan = ?
    """, (ma_tai_khoan,))
    items = cursor.fetchall()

    if not items:
        flash("Giỏ hàng trống.")
        return redirect(url_for('cart'))

    # Tính tổng tiền
    tong_tien = sum([item[1] * item[2] for item in items])

    # Tạo hóa đơn
    cursor.execute("INSERT INTO HoaDon (MaNguoiDung, TongTien) VALUES (?, ?)", (ma_nguoidung, tong_tien))
    conn.commit()

    # Lấy mã hóa đơn vừa tạo
    cursor.execute("SELECT @@IDENTITY")
    ma_hoadon = int(cursor.fetchone()[0])

    # Thêm chi tiết hóa đơn + lưu vào lịch sử mua hàng
    for product_id, don_gia, so_luong in items:
        cursor.execute(
            "INSERT INTO ChiTietHoaDon (MaHoaDon, ProductID, SoLuong, DonGia) VALUES (?, ?, ?, ?)",
            (ma_hoadon, product_id, so_luong, don_gia)
        )
        cursor.execute(
            "INSERT INTO LichSuMuaHang (MaTaiKhoan, ProductID, SoLuong) VALUES (?, ?, ?)",
            (ma_tai_khoan, product_id, so_luong)
        )

    # Xóa giỏ hàng
    cursor.execute("DELETE FROM GioHang WHERE MaTaiKhoan = ?", (ma_tai_khoan,))
    conn.commit()
    conn.close()

    flash("Thanh toán thành công!")
    return redirect(url_for('index'))


@app.context_processor
def inject_cart_info():
    def get_cart_count(ma_tai_khoan):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM GioHang WHERE MaTaiKhoan = ?", (ma_tai_khoan,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    return dict(get_cart_count=get_cart_count)



if __name__ == '__main__':
    app.run(debug=True, port=8000)



