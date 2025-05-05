from flask import Flask, render_template
from database.db_connection import get_products
from database.data_processing import load_transactions, preprocess_data
from analysis.apriori_analysis import run_apriori

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def index():
    # Lấy danh sách sản phẩm từ cơ sở dữ liệu
    products = get_products()
    return render_template('index.html', products=products)

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
@app.route('/category/<category>')
def category(category):
    # Lấy danh sách sản phẩm theo danh mục
    from database.db_connection import get_products_by_category
    products = get_products_by_category(category)
    return render_template('category.html', category=category, products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    from database.db_connection import get_product_by_id
    product = get_product_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)