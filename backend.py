import sqlite3
import datetime

DB = "food_db.db"

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def exe_query(query, param = None, commit = False, fetch_one = False):
    conn = connect()
    cur = conn.cursor()
    result = None
    
    try:
        if param:
            cur.execute(query, param)
        else:
            cur.execute(query)

        if commit:
            conn.commit()
            result = True
        elif fetch_one:
            result = cur.fetchone()        
        else:
            result = cur.fetchall()
    
    except sqlite3.Error as e:
        print(e)
        if commit:
            conn.rollback()
        result = None
    
    finally:
        conn.close()
    
    return result

class Cus_manager: 
    def add(self, name, phone):
        query = "INSERT INTO Customers (cus_name, cus_phone) VALUES (?,?)"
        return exe_query(query, (name, phone), commit = True)
    
    def remove(self, cus_id):
        query = "DELETE FROM Customers WHERE cus_id = ?"
        return exe_query(query, (cus_id,), commit = True)
    
    def find_cus(self, phone):
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers WHERE cus_phone = ?"
        return exe_query(query, (phone,), fetch_one = True)
    
    def list_cus(self):
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers"
        return exe_query(query, ())
    
class Emp_manager:
    def add(self, name):
        query = "INSERT INTO Employees (emp_name) VALUES (?)"
        return exe_query(query, (name,), commit = True)
    
    def remove(self, emp_id):
        query = "DELETE FROM Employees WHERE emp_id = ?"
        return exe_query(query, (emp_id,), commit = True)
    
    def list_emp(self):
        query = "SELECT emp_id, emp_name FROM Employees"
        return exe_query(query, ())
    
    def count_bill(self):
        query = """SELECT Employeess.emp_id, emp_name
        COUNT(Bills.bill_id) AS orders_served
        FROM Employees
        LEFT JOIN Bills ON Employees.emp_id = Bills.emp_id
        GROUP BY emp_id, emp_name
        ODRDER BY orders_served"""
        return exe_query(query, ())
    
class Dish_manager:
    def add(self, name):
        query = "INSERT INTO  Dishes (dish_name) VALUES (?)"
        return exe_query(query, (name,), commit = True)
    
    def remove(self, dish_id):
        query = "DELETE FROM Dishes WHERE dish_id = ?"
        return exe_query(query, (dish_id,), commit = True)
    
    def list_dishes(self):
        query = "SELECT dish_id, dish_name, recipe, cooking_time, dish_price FROM Dishes"
        return exe_query(query, ())


class Order_manager:
    def create_orders(self, dish_req_in, total_price, cus_id):
        order_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        status = "Chờ duyệt"
        
        conn = connect()
        cur = conn.cursor()
        order_id = None
        try:
            cur.execute("""
                INSERT INTO Orders (dish_req, total_price, order_time, status, cus_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (dish_req_in, total_price, order_time, status, cus_id))
            order_id = cur.lastrowid
            conn.commit()
        except sqlite3.Error as e:
            print(f"Order Creation Error: {e}")
            conn.rollback()
        finally:
            conn.close()
        
        return order_id
    
    def create_bill(self, order_id, emp_id, shipper_id, total_amount):
        bill_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Bills (order_id, emp_id, shipper_id, total_amount, bill_time) 
        VALUES (?, ?, ?, ?, ?)
        """
        return exe_query(query, (order_id, emp_id, shipper_id, total_amount, bill_time), commit=True)
    
    def add_delivery(self, order_id, shipper_id, delivery_addr, distance, fee):
        delivery_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Deliveries (order_id, shipper_id, delivery_time, delivery_addr, distance, fee) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return exe_query(query, (order_id, shipper_id, delivery_time, delivery_addr, distance, fee), commit=True)
    
    def get_all_orders_details(self):
        query = """
        SELECT 
            o.order_id, o.dish_req, o.total_price, o.order_time, o.status,
            c.cus_name, c.cus_phone
        FROM 
            Orders o
        JOIN 
            Customers c ON o.cus_id = c.cus_id
        ORDER BY 
            o.order_time DESC
        """
        return exe_query(query)
    
    def update_status(self, order_id, status):
        query = "UPDATE Orders SET status = ? WHERE order_id = ?"
        return exe_query(query, (status, order_id), commit=True)

    def get_delivery_info(self, order_id):
        query = """
        SELECT 
            d.delivery_addr, d.distance, d.fee, s.shipper_info
        FROM 
            Deliveries d
        JOIN 
            Shippers s ON d.shipper_id = s.shipper_id
        WHERE 
            d.order_id = ?
        """
        return exe_query(query, (order_id,), fetch_one=True)

class Ingredient_manager:
    def add(self, name, stock, unit, expiry, suppliers):
        query = "INSERT INTO Ingredients (ingre_name, stock, unit, expiry, suppliers) VALUES (?, ?, ?, ?, ?)"
        return exe_query(query, (name, stock, unit, expiry, suppliers), commit=True)
    
    def get_all(self):
        query = "SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers FROM Ingredients"
        return exe_query(query, ())
    
    def update_stock(self, ingre_id, new_stock):
        query = "UPDATE Ingredients SET stock = ? WHERE ingre_id = ?"
        return exe_query(query, (new_stock, ingre_id), commit=True)
    
    def used_stock(self):
        #cai nay lam sau luoi qua
        pass

class Shipper_manager:
    def get_all(self):
        query = "SELECT shipper_id, shipper_info FROM Shippers"
        return exe_query(query, ())

class System:
    def __init__(self):
        self.cus_manager=Cus_manager()
        self.emp_manager=Emp_manager()
        self.dish_manager=Dish_manager()
        self.ingr_manager=Ingredient_manager()
        self.shipper_manager=Shipper_manager()
        self.order_manager=Order_manager()

if __name__=="__main__":
    cus_manager = Order_manager()
    while True:
        print("1. add customer")
        print("2. remove customer")
        print("3. find customer")
        print("4. list customers")
        print("q. back")
        choice = input("chọn: ")
        
        if choice == "1":
            name = input("tên: ")
            phone = input("dth: ")
            cus_manager.add(name, phone)
        elif choice == "2":
            cus_id = int(input("Customer ID to remove: "))
            cus_manager.remove(cus_id)
        elif choice == "3":
            phone = input("Customer phone: ")
            result = cus_manager.find_cus(phone)
            print(result)
        elif choice == "4":
            result = cus_manager.get_all_order_details()
            data = [dict(resul) for resul in result]
            print(len(data))
        elif choice == "q":
            break