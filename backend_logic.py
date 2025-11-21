import sqlite3
import datetime

DATABASE_NAME = "food_db.db"

# --- 1. Database Connection Helpers (CORRECTED) ---

def connect():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Set row_factory to sqlite3.Row for dictionary-like access to results
    conn.row_factory = sqlite3.Row 
    return conn

def execute_query(query, params=(), fetch_one=False, commit=False):
    """
    Executes a query and handles connection, cursor, and closing.
    (CORRECTED to remove 'return' from 'finally')
    """
    conn = connect()
    cur = conn.cursor()
    result = None # Initialize result
    try:
        cur.execute(query, params)
        
        if commit:
            conn.commit()
            result = True # Set result to True for successful commit
        
        elif fetch_one:
            result = cur.fetchone()
        else:
            result = cur.fetchall()
            
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        if commit:
            conn.rollback()
        result = None # Explicitly set result to None on error
        
    finally:
        conn.close() # The 'finally' block *only* closes the connection
    
    # The return statement is now *outside* the finally block
    return result

# --- 2. CustomerManager Class ---

class CustomerManager:
    """Handles all logic for the Customers table."""
    
    def add(self, name, phone):
        """Inserts a new customer. Returns True on success."""
        query = "INSERT INTO Customers (cus_name, cus_phone) VALUES (?, ?)"
        return execute_query(query, (name, phone), commit=True)

    def get_all(self):
        """Retrieves all customer records."""
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers"
        return execute_query(query)

    def get_by_phone(self, phone):
        """Finds a customer by phone number. Returns the record or None."""
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers WHERE cus_phone = ?"
        return execute_query(query, (phone,), fetch_one=True)

    def delete(self, cus_id):
        """Deletes a customer by ID."""
        query = "DELETE FROM Customers WHERE cus_id = ?"
        return execute_query(query, (cus_id,), commit=True)

# --- 3. EmployeeManager Class ---

class EmployeeManager:
    """Handles all logic for the Employees table."""
    
    def add(self, name):
        """Inserts a new employee. Returns True on success."""
        query = "INSERT INTO Employees (emp_name) VALUES (?)"
        return execute_query(query, (name,), commit=True)

    def get_all(self):
        """Retrieves all employee records."""
        query = "SELECT emp_id, emp_name FROM Employees"
        return execute_query(query)

    def delete(self, emp_id):
        """Deletes an employee by ID."""
        query = "DELETE FROM Employees WHERE emp_id = ?"
        return execute_query(query, (emp_id,), commit=True)

    def get_order_stats(self):
        """Retrieves employee name and the count of bills (orders served)."""
        query = """
        SELECT 
            e.emp_id, e.emp_name, 
            COUNT(b.bill_id) AS orders_served
        FROM 
            Employees e
        LEFT JOIN 
            Bills b ON e.emp_id = b.emp_id
        GROUP BY 
            e.emp_id, e.emp_name
        ORDER BY 
            orders_served DESC
        """
        return execute_query(query)

# --- 4. DishManager Class ---

class DishManager:
    """Handles all logic for the Dishes table."""
    
    def add(self, name, recipe, cooking_time, price):
        """Inserts a new dish."""
        query = "INSERT INTO Dishes (dish_name, recipe, cooking_time, dish_price) VALUES (?, ?, ?, ?)"
        return execute_query(query, (name, recipe, cooking_time, price), commit=True)

    def get_all(self):
        """Retrieves all dish records."""
        query = "SELECT dish_id, dish_name, recipe, cooking_time, dish_price FROM Dishes"
        return execute_query(query)

    def delete(self, dish_id):
        """Deletes a dish by ID."""
        query = "DELETE FROM Dishes WHERE dish_id = ?"
        return execute_query(query, (dish_id,), commit=True)

# --- 5. IngredientManager Class ---

class IngredientManager:
    """Handles all logic for the Ingredients table."""
    
    def add(self, name, stock, unit, expiry, suppliers):
        """Inserts a new ingredient."""
        query = "INSERT INTO Ingredients (ingre_name, stock, unit, expiry, suppliers) VALUES (?, ?, ?, ?, ?)"
        return execute_query(query, (name, stock, unit, expiry, suppliers), commit=True)

    def get_all(self):
        """RetrieVes all ingredient records."""
        query = "SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers FROM Ingredients"
        return execute_query(query)

    def update_stock(self, ingre_id, new_stock):
        """Updates the stock level of an ingredient."""
        query = "UPDATE Ingredients SET stock = ? WHERE ingre_id = ?"
        return execute_query(query, (new_stock, ingre_id), commit=True)

    def deduct_stock_for_order(self, dish_req_string):
        """
        Simulated function to deduct stock.
        In a real system, this would be much more complex.
        """
        print(f"INFO: Simulating stock deduction for request: {dish_req_string}")
        return True # Always succeed for now

# --- 6. ShipperManager Class ---

class ShipperManager:
    """Handles all logic for the Shippers table."""
    
    def get_all(self):
        """Retrieves all shippers."""
        query = "SELECT shipper_id, shipper_info FROM Shippers"
        return execute_query(query)

# --- 7. OrderManager Class ---

class OrderManager:
    """Handles logic for Orders, Bills, and Deliveries."""
    
    def create_order(self, dish_req_string, total_price, cus_id):
        """
        Inserts a new order into Orders table. Returns the new order_id on success.
        """
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Pending"
        
        # We need to handle the connection manually for this one case 
        # to reliably get the 'lastrowid'.
        conn = connect()
        cur = conn.cursor()
        order_id = None
        try:
            cur.execute("""
                INSERT INTO Orders (dish_req, total_price, order_time, status, cus_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (dish_req_string, total_price, order_time, status, cus_id))
            order_id = cur.lastrowid
            conn.commit()
        except sqlite3.Error as e:
            print(f"Order Creation Error: {e}")
            conn.rollback()
        finally:
            conn.close()
            
        return order_id # Return the ID (or None if it failed)

    def create_bill(self, order_id, emp_id, shipper_id, total_amount):
        """Inserts a bill record."""
        bill_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Bills (order_id, emp_id, shipper_id, total_amount, bill_time) 
        VALUES (?, ?, ?, ?, ?)
        """
        return execute_query(query, (order_id, emp_id, shipper_id, total_amount, bill_time), commit=True)

    def add_delivery(self, order_id, shipper_id, delivery_addr, distance, fee):
        """Inserts new delivery record."""
        delivery_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Deliveries (order_id, shipper_id, delivery_time, delivery_addr, distance, fee) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (order_id, shipper_id, delivery_time, delivery_addr, distance, fee), commit=True)

    def get_all_orders_details(self):
        """Retrieves all orders with linked customer name."""
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
        return execute_query(query)

    def update_status(self, order_id, status):
        """Updates the status of an order."""
        query = "UPDATE Orders SET status = ? WHERE order_id = ?"
        return execute_query(query, (status, order_id), commit=True)

    def get_delivery_info(self, order_id):
        """Retrieves delivery details for a specific order."""
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
        return execute_query(query, (order_id,), fetch_one=True)