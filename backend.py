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
        query = "INSERT INTO CUstomers (cus_name, cus_phone) VALUES (?,?)"
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

cus_manager = Cus_manager()
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
        result = cus_manager.list_cus()
        for row in result:
            print(dict(row))
    elif choice == "q":
        break
