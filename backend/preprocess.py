import pandas as pd

# Đọc dữ liệu từ file Excel
df = pd.read_excel('data/giao_dich.xlsx')

# Hiển thị thông tin tổng quan
print("Thông tin dữ liệu ban đầu:")
print(df.info())
print(df.head())

# Xóa dòng bị thiếu dữ liệu
df = df.dropna()

# Xóa dòng trùng lặp
df = df.drop_duplicates()

# Chuẩn hóa tên sản phẩm (nếu có cột 'ten_san_pham')
if 'ten_san_pham' in df.columns:
    df['ten_san_pham'] = df['ten_san_pham'].str.lower().str.strip()
elif 'ProductName' in df.columns:
    df['ProductName'] = df['ProductName'].str.lower().str.strip()

# Lưu lại file đã xử lý
df.to_excel('data/giao_dich_clean.xlsx', index=False)

print("Tiền xử lý xong! File lưu tại data/giao_dich_clean.xlsx")
