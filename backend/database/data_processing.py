import pandas as pd
from database.db_connection import get_connection

def load_transactions():
    conn = get_connection()
    query = "SELECT * FROM Transactions"
    transactions = pd.read_sql(query, conn)
    conn.close()
    return transactions

def preprocess_data(transactions):
    # Xử lý dữ liệu thiếu
    transactions.fillna({'ColumnName': 'DefaultValue'}, inplace=True)

    # Loại bỏ dữ liệu trùng lặp
    transactions.drop_duplicates(inplace=True)

    # Chuẩn hóa dữ liệu (ví dụ: chuyển đổi ngày tháng)
    transactions['TransactionDate'] = pd.to_datetime(transactions['TransactionDate'])

    return transactions