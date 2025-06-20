import pandas as pd

# Đọc dữ liệu đã làm sạch
df = pd.read_excel('data/GiaoDich_clean.xlsx')

# Lấy tên cột đầu tiên (vì file chỉ có 1 cột)
col_name = df.columns[0]

rows = []
for idx, row in df.iterrows():
    ma_hoa_don = idx + 1
    for product in str(row[col_name]).split(','):
        product = product.strip()
        if product:  # Bỏ qua sản phẩm rỗng
            rows.append({'MaHoaDon': ma_hoa_don, 'ProductID': product})

# Xuất ra file Excel hoặc CSV để import vào SQL Server
pd.DataFrame(rows).to_excel('data/chi_tiet_hoa_don.xlsx', index=False)


