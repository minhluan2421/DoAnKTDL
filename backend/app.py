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

if __name__ == '__main__':
    app.run(debug=True, port=8000)