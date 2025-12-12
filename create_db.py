import sqlite3

conn = sqlite3.connect("food_db.db")
cur = conn.cursor()

tables = ["Bills", "Deliveries", "Orders", "Dishes", "Ingredients", "Customers", "Shippers", "Employees"]
for t in tables:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

cur.execute("""
CREATE TABLE Ingredients (
    ingre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingre_name TEXT NOT NULL,
    stock INTEGER,
    unit TEXT,
    expiry TEXT,
    suppliers TEXT
)
""")

cur.execute("""
CREATE TABLE Dishes (
    dish_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_name TEXT NOT NULL,
    cooking_time INTEGER,
    dish_price REAL
)
""")

cur.execute("""
CREATE TABLE Customers (
    cus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cus_name TEXT NOT NULL,
    cus_phone TEXT
)
""")

cur.execute("""
CREATE TABLE Shippers (
    shipper_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipper_info TEXT
)
""")

cur.execute("""
CREATE TABLE Employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_req TEXT,
    total_price REAL,
    order_time TEXT,
    status TEXT,
    cus_id INTEGER,
    FOREIGN KEY (cus_id) REFERENCES Customers(cus_id)
)
""")

cur.execute("""
CREATE TABLE Deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    shipper_id INTEGER,
    delivery_time TEXT,
    delivery_addr TEXT,
    distance REAL,
    fee REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (shipper_id) REFERENCES Shippers(shipper_id)
)
""")

cur.execute("""
CREATE TABLE Bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    emp_id INTEGER,
    shipper_id INTEGER,
    total_amount REAL,
    bill_time TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (emp_id) REFERENCES Employees(emp_id),
    FOREIGN KEY (shipper_id) REFERENCES Shippers(shipper_id)
)
""")

cur.execute("""
CREATE TABLE Dish_Ingredients (
    dish_id INTEGER,
    ingre_id INTEGER,
    quantity REAL,
    PRIMARY KEY (dish_id, ingre_id),
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
    FOREIGN KEY (ingre_id) REFERENCES Ingredients(ingre_id)
)
""")

cur.execute("INSERT INTO Dish_Ingredients VALUES (1, 2, 0.2)")
cur.execute("INSERT INTO Dish_Ingredients VALUES (1, 3, 0.05)")
cur.execute("INSERT INTO Dish_Ingredients VALUES (1, 1, 0.1)")
cur.execute("INSERT INTO Dish_Ingredients VALUES (2, 3, 0.3)")
cur.execute("INSERT INTO Dish_Ingredients VALUES (2, 1, 0.2)")

cur.executemany("INSERT INTO Ingredients (ingre_name, stock, unit, expiry, suppliers) VALUES (?, ?, ?, ?, ?)", [
    ("cà chua", 100, "kg", "2025-12-31", "Nhà ngoại"),
    ("Thịt gà", 50, "kg", "2025-11-20", "Nhà nội"),
    ("Phô mai", 30, "kg", "2025-12-15", "Nhà trồng"),
])

cur.executemany("INSERT INTO Dishes (dish_name, cooking_time, dish_price) VALUES (?, ?, ?)", [
    ("Burger gà", 15, 60000),
    ("Pizza", 20, 100000),
])

cur.executemany("INSERT INTO Customers (cus_name, cus_phone) VALUES (?, ?)", [
    ("Hello", "123456789"),
    ("Hi", "987654321"),
])

cur.executemany("INSERT INTO Shippers (shipper_info) VALUES (?)", [
    ("Giao hàng nhanh Delivery",),
    ("Giao hàng nhanh hơn Express",),
])

cur.executemany("INSERT INTO Employees (emp_name) VALUES (?)", [
    ("Quản lí 1",),
    ("Nhân viên 1",),
])


conn.commit()
conn.close()

print("food_db.db tạo thành công")
