import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Đọc lại transactions từ bước trên
df = pd.read_excel('data/chitiethoadon2.xlsx')
transactions = df.groupby('MaHoaDon')['ProductID'].apply(lambda x: list(x)).tolist()

# Mã hóa dữ liệu
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_tf = pd.DataFrame(te_ary, columns=te.columns_)

# Khai phá tập phổ biến
frequent_itemsets = apriori(df_tf, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Hiển thị các luật gợi ý mua kèm
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Chuyển frozenset sang list để lưu ra file CSV
rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_csv('data/rules.csv', index=False)
