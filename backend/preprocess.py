import pandas as pd
import re
import os

# Đảm bảo thư mục đầu ra tồn tại
output_dir = 'data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Đọc dữ liệu từ file Excel
try:
    df = pd.read_excel('data/GiaoDich.xlsx', header=None)
    print("Đã đọc file thành công!")
except FileNotFoundError:
    print("Không tìm thấy file 'data/GiaoDich.xlsx'. Vui lòng kiểm tra đường dẫn file.")
    exit()
except Exception as e:
    print(f"Lỗi khi đọc file: {e}")
    exit()

# Hiển thị thông tin tổng quan
print("Thông tin dữ liệu ban đầu:")
print(df.info())
print("\n5 dòng đầu tiên:")
print(df.head())

# Xóa các cột hoàn toàn rỗng (do dấu phẩy thừa ở cuối dòng)
df = df.dropna(how='all', axis=1)

# Xóa các dòng hoàn toàn rỗng
df = df.dropna(how='all')

# Xóa các dòng trùng lặp
df = df.drop_duplicates()

# Hàm chuẩn hóa và làm sạch văn bản
def clean_text(text):
    if pd.isna(text):
        return text
    # Loại bỏ ký tự đặc biệt, giữ chữ, số, khoảng trắng
    text = re.sub(r'[^\w\s]', '', str(text))
    # Chuyển về chữ thường và loại bỏ khoảng trắng thừa
    return text.strip()

# Áp dụng làm sạch cho tất cả các cột
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# Loại bỏ các cột mà tất cả giá trị là rỗng hoặc NaN sau khi làm sạch
df = df.loc[:, (df != '').any(axis=0) & df.notna().any(axis=0)]

# Chuẩn hóa tên sản phẩm (nếu có cột 'ten_san_pham')
if 'ten_san_pham' in df.columns:
    df['ten_san_pham'] = df['ten_san_pham'].str.lower().str.strip()
elif 'ProductName' in df.columns:
    df['ProductName'] = df['ProductName'].str.lower().str.strip()

# Hiển thị thông tin dữ liệu sau khi xử lý
print("\nThông tin dữ liệu sau khi xử lý:")
print(df.info())
print("\n5 dòng đầu tiên sau khi xử lý:")
print(df.head())

# Lưu lại file đã xử lý
output_path = 'data/GiaoDich_clean.xlsx'
try:
    df.to_excel(output_path, index=False)
    print(f"\nTiền xử lý xong! File lưu tại {output_path}")
except Exception as e:
    print(f"Lỗi khi lưu file: {e}")

# Thông báo số lượng dòng đã bị xóa
initial_rows = pd.read_excel('data/GiaoDich.xlsx', header=None).shape[0]
final_rows = df.shape[0]
print(f"\nSố dòng ban đầu: {initial_rows}")
print(f"Số dòng sau khi xử lý: {final_rows}")
print(f"Số dòng đã xóa (trùng lặp hoặc rỗng): {initial_rows - final_rows}")

