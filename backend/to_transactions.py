import pandas as pd

# Đọc file chi tiết hóa đơn
df = pd.read_excel('data/chi_tiet_hoa_don.xlsx')

# Gom nhóm theo MaHoaDon, mỗi hóa đơn là một list sản phẩm
transactions = df.groupby('MaHoaDon')['ProductID'].apply(lambda x: list(x)).tolist()

# In thử 5 giao dịch đầu tiên
print("5 giao dịch đầu tiên:")
for t in transactions[:5]:
    print(t)