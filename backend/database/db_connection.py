import pyodbc

def get_connection():
    # Kết nối đến SQL Server với tài khoản riêng
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-5O90F68\SQLEXPRESS;"  # Thay bằng tên server của bạn
        "Database=ElectronicsStore;"  # Tên cơ sở dữ liệu
        # "UID=sa;"  # Thay bằng tên tài khoản SQL Server của bạn
        # "PWD=123456;"  # Thay bằng mật khẩu của bạn
    )
    return conn

def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, ProductName, Price, ImagePath FROM Products")
    products = cursor.fetchall()
    conn.close()
    # Dùng đường dẫn tuyệt đối
    products = [
        (product[0], product[1], product[2], f"/static/{product[3]}") for product in products
    ]
    return products

def get_products_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT ProductID, ProductName, Price, ImagePath FROM Products WHERE Category = ?"
    cursor.execute(query, (category,))
    products = cursor.fetchall()
    conn.close()
    # Thêm tiền tố 'static/' vào đường dẫn ảnh
    products = [
        (product[0], product[1], product[2], f"/static/{product[3]}") for product in products
    ]
    return products

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT ProductID, ProductName, Price, ImagePath, Description
        FROM Products
        WHERE ProductID = ?
    """
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product
