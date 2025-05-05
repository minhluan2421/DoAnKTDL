from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def run_apriori(transactions):
    # Chuyển đổi dữ liệu giao dịch thành dạng ma trận
    transactions_pivot = transactions.pivot_table(index='TransactionID', columns='ProductID', aggfunc='size', fill_value=0)

    # Tìm tập phổ biến
    frequent_itemsets = apriori(transactions_pivot, min_support=0.1, use_colnames=True)

    # Tìm luật kết hợp
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

    return rules