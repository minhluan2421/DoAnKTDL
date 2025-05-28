import pandas as pd

# Đọc dữ liệu đã làm sạch
df = pd.read_excel('data/giao_dich_clean.xlsx')

# Giả sử mỗi dòng là 1 hóa đơn, cột 'PurchasedItems' chứa danh sách mã sản phẩm cách nhau bởi dấu phẩy
rows = []
for idx, row in df.iterrows():
    ma_hoa_don = idx + 1  # hoặc dùng row['transaction_id'] nếu có
    for product in str(row['PurchasedItems']).split(','):
        rows.append({'MaHoaDon': ma_hoa_don, 'ProductID': product.strip()})

# Xuất ra file Excel hoặc CSV để import vào SQL Server
pd.DataFrame(rows).to_excel('data/chi_tiet_hoa_don.xlsx', index=False)



