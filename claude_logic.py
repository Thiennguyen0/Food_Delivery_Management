"""
Enhanced Food Management System Backend
Improved version with better error handling, logging, type hints, and features
"""

import sqlite3
import datetime
import logging
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum

# --- Configuration ---
DATABASE_NAME = "food_db.db"

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Enums for Type Safety ---
class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "Pending"
    PREPARING = "Preparing"
    READY = "Ready"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

# --- Data Classes ---
@dataclass
class Customer:
    """Customer data class"""
    cus_id: Optional[int]
    cus_name: str
    cus_phone: str

@dataclass
class Employee:
    """Employee data class"""
    emp_id: Optional[int]
    emp_name: str

@dataclass
class Dish:
    """Dish data class"""
    dish_id: Optional[int]
    dish_name: str
    recipe: str
    cooking_time: int
    dish_price: float

@dataclass
class Ingredient:
    """Ingredient data class"""
    ingre_id: Optional[int]
    ingre_name: str
    stock: float
    unit: str
    expiry: str
    suppliers: str

# --- Database Connection Manager ---
class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_name: str = DATABASE_NAME):
        self.db_name = db_name
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(
        self, 
        query: str, 
        params: Tuple = (), 
        fetch_one: bool = False, 
        commit: bool = False
    ) -> Optional[Any]:
        """
        Executes a query with proper error handling
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch_one: Whether to fetch single result
            commit: Whether to commit changes
            
        Returns:
            Query results or success status
        """
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                
                if commit:
                    conn.commit()
                    return True
                elif fetch_one:
                    return cur.fetchone()
                else:
                    return cur.fetchall()
                    
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity constraint violation: {e}")
            return None
        except sqlite3.Error as e:
            logger.error(f"Database error executing query: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def execute_with_lastrowid(self, query: str, params: Tuple = ()) -> Optional[int]:
        """
        Executes INSERT query and returns last inserted row ID
        
        Args:
            query: SQL INSERT query
            params: Query parameters
            
        Returns:
            Last inserted row ID or None on failure
        """
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                last_id = cur.lastrowid
                conn.commit()
                logger.info(f"Successfully inserted record with ID: {last_id}")
                return last_id
        except sqlite3.Error as e:
            logger.error(f"Error inserting record: {e}")
            return None

# --- Manager Classes ---

class CustomerManager:
    """Handles all customer-related operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, name: str, phone: str) -> bool:
        """
        Adds a new customer
        
        Args:
            name: Customer name
            phone: Customer phone number
            
        Returns:
            True if successful, False otherwise
        """
        if not name or not phone:
            logger.warning("Customer name and phone are required")
            return False
        
        # Check if customer already exists
        if self.get_by_phone(phone):
            logger.warning(f"Customer with phone {phone} already exists")
            return False
        
        query = "INSERT INTO Customers (cus_name, cus_phone) VALUES (?, ?)"
        result = self.db.execute_query(query, (name, phone), commit=True)
        
        if result:
            logger.info(f"Added customer: {name} ({phone})")
        return bool(result)
    
    def get_all(self) -> List[sqlite3.Row]:
        """Retrieves all customers"""
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers ORDER BY cus_name"
        return self.db.execute_query(query) or []
    
    def get_by_phone(self, phone: str) -> Optional[sqlite3.Row]:
        """Finds customer by phone number"""
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers WHERE cus_phone = ?"
        return self.db.execute_query(query, (phone,), fetch_one=True)
    
    def get_by_id(self, cus_id: int) -> Optional[sqlite3.Row]:
        """Finds customer by ID"""
        query = "SELECT cus_id, cus_name, cus_phone FROM Customers WHERE cus_id = ?"
        return self.db.execute_query(query, (cus_id,), fetch_one=True)
    
    def update(self, cus_id: int, name: str, phone: str) -> bool:
        """Updates customer information"""
        query = "UPDATE Customers SET cus_name = ?, cus_phone = ? WHERE cus_id = ?"
        result = self.db.execute_query(query, (name, phone, cus_id), commit=True)
        
        if result:
            logger.info(f"Updated customer ID {cus_id}")
        return bool(result)
    
    def delete(self, cus_id: int) -> bool:
        """Deletes a customer"""
        query = "DELETE FROM Customers WHERE cus_id = ?"
        result = self.db.execute_query(query, (cus_id,), commit=True)
        
        if result:
            logger.info(f"Deleted customer ID {cus_id}")
        return bool(result)
    
    def search(self, search_term: str) -> List[sqlite3.Row]:
        """Searches customers by name or phone"""
        query = """
        SELECT cus_id, cus_name, cus_phone 
        FROM Customers 
        WHERE cus_name LIKE ? OR cus_phone LIKE ?
        ORDER BY cus_name
        """
        pattern = f"%{search_term}%"
        return self.db.execute_query(query, (pattern, pattern)) or []


class EmployeeManager:
    """Handles all employee-related operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, name: str) -> bool:
        """Adds a new employee"""
        if not name:
            logger.warning("Employee name is required")
            return False
        
        query = "INSERT INTO Employees (emp_name) VALUES (?)"
        result = self.db.execute_query(query, (name,), commit=True)
        
        if result:
            logger.info(f"Added employee: {name}")
        return bool(result)
    
    def get_all(self) -> List[sqlite3.Row]:
        """Retrieves all employees"""
        query = "SELECT emp_id, emp_name FROM Employees ORDER BY emp_name"
        return self.db.execute_query(query) or []
    
    def get_by_id(self, emp_id: int) -> Optional[sqlite3.Row]:
        """Finds employee by ID"""
        query = "SELECT emp_id, emp_name FROM Employees WHERE emp_id = ?"
        return self.db.execute_query(query, (emp_id,), fetch_one=True)
    
    def update(self, emp_id: int, name: str) -> bool:
        """Updates employee information"""
        query = "UPDATE Employees SET emp_name = ? WHERE emp_id = ?"
        result = self.db.execute_query(query, (name, emp_id), commit=True)
        
        if result:
            logger.info(f"Updated employee ID {emp_id}")
        return bool(result)
    
    def delete(self, emp_id: int) -> bool:
        """Deletes an employee"""
        query = "DELETE FROM Employees WHERE emp_id = ?"
        result = self.db.execute_query(query, (emp_id,), commit=True)
        
        if result:
            logger.info(f"Deleted employee ID {emp_id}")
        return bool(result)
    
    def get_order_stats(self) -> List[sqlite3.Row]:
        """Retrieves employee performance statistics"""
        query = """
        SELECT 
            e.emp_id, 
            e.emp_name, 
            COUNT(b.bill_id) AS orders_served,
            COALESCE(SUM(b.total_amount), 0) AS total_sales
        FROM 
            Employees e
        LEFT JOIN 
            Bills b ON e.emp_id = b.emp_id
        GROUP BY 
            e.emp_id, e.emp_name
        ORDER BY 
            orders_served DESC, total_sales DESC
        """
        return self.db.execute_query(query) or []


class DishManager:
    """Handles all dish-related operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(self, name: str, recipe: str, cooking_time: int, price: float) -> bool:
        """Adds a new dish"""
        if not name or price <= 0:
            logger.warning("Invalid dish data")
            return False
        
        query = """
        INSERT INTO Dishes (dish_name, recipe, cooking_time, dish_price) 
        VALUES (?, ?, ?, ?)
        """
        result = self.db.execute_query(
            query, (name, recipe, cooking_time, price), commit=True
        )
        
        if result:
            logger.info(f"Added dish: {name} (${price})")
        return bool(result)
    
    def get_all(self) -> List[sqlite3.Row]:
        """Retrieves all dishes"""
        query = """
        SELECT dish_id, dish_name, recipe, cooking_time, dish_price 
        FROM Dishes 
        ORDER BY dish_name
        """
        return self.db.execute_query(query) or []
    
    def get_by_id(self, dish_id: int) -> Optional[sqlite3.Row]:
        """Finds dish by ID"""
        query = """
        SELECT dish_id, dish_name, recipe, cooking_time, dish_price 
        FROM Dishes 
        WHERE dish_id = ?
        """
        return self.db.execute_query(query, (dish_id,), fetch_one=True)
    
    def update(
        self, dish_id: int, name: str, recipe: str, cooking_time: int, price: float
    ) -> bool:
        """Updates dish information"""
        query = """
        UPDATE Dishes 
        SET dish_name = ?, recipe = ?, cooking_time = ?, dish_price = ? 
        WHERE dish_id = ?
        """
        result = self.db.execute_query(
            query, (name, recipe, cooking_time, price, dish_id), commit=True
        )
        
        if result:
            logger.info(f"Updated dish ID {dish_id}")
        return bool(result)
    
    def delete(self, dish_id: int) -> bool:
        """Deletes a dish"""
        query = "DELETE FROM Dishes WHERE dish_id = ?"
        result = self.db.execute_query(query, (dish_id,), commit=True)
        
        if result:
            logger.info(f"Deleted dish ID {dish_id}")
        return bool(result)
    
    def search(self, search_term: str) -> List[sqlite3.Row]:
        """Searches dishes by name"""
        query = """
        SELECT dish_id, dish_name, recipe, cooking_time, dish_price 
        FROM Dishes 
        WHERE dish_name LIKE ? OR recipe LIKE ?
        ORDER BY dish_name
        """
        pattern = f"%{search_term}%"
        return self.db.execute_query(query, (pattern, pattern)) or []
    
    def get_popular_dishes(self, limit: int = 10) -> List[sqlite3.Row]:
        """Gets most ordered dishes"""
        query = """
        SELECT 
            d.dish_id, d.dish_name, d.dish_price,
            COUNT(*) as order_count
        FROM Dishes d
        JOIN Orders o ON o.dish_req LIKE '%' || d.dish_name || '%'
        GROUP BY d.dish_id, d.dish_name, d.dish_price
        ORDER BY order_count DESC
        LIMIT ?
        """
        return self.db.execute_query(query, (limit,)) or []


class IngredientManager:
    """Handles all ingredient-related operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add(
        self, name: str, stock: float, unit: str, expiry: str, suppliers: str
    ) -> bool:
        """Adds a new ingredient"""
        if not name or stock < 0:
            logger.warning("Invalid ingredient data")
            return False
        
        query = """
        INSERT INTO Ingredients (ingre_name, stock, unit, expiry, suppliers) 
        VALUES (?, ?, ?, ?, ?)
        """
        result = self.db.execute_query(
            query, (name, stock, unit, expiry, suppliers), commit=True
        )
        
        if result:
            logger.info(f"Added ingredient: {name} ({stock} {unit})")
        return bool(result)
    
    def get_all(self) -> List[sqlite3.Row]:
        """Retrieves all ingredients"""
        query = """
        SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers 
        FROM Ingredients 
        ORDER BY ingre_name
        """
        return self.db.execute_query(query) or []
    
    def get_by_id(self, ingre_id: int) -> Optional[sqlite3.Row]:
        """Finds ingredient by ID"""
        query = """
        SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers 
        FROM Ingredients 
        WHERE ingre_id = ?
        """
        return self.db.execute_query(query, (ingre_id,), fetch_one=True)
    
    def update_stock(self, ingre_id: int, new_stock: float) -> bool:
        """Updates ingredient stock level"""
        if new_stock < 0:
            logger.warning(f"Invalid stock level: {new_stock}")
            return False
        
        query = "UPDATE Ingredients SET stock = ? WHERE ingre_id = ?"
        result = self.db.execute_query(query, (new_stock, ingre_id), commit=True)
        
        if result:
            logger.info(f"Updated stock for ingredient ID {ingre_id} to {new_stock}")
        return bool(result)
    
    def update(
        self, ingre_id: int, name: str, stock: float, unit: str, expiry: str, suppliers: str
    ) -> bool:
        """Updates ingredient information"""
        query = """
        UPDATE Ingredients 
        SET ingre_name = ?, stock = ?, unit = ?, expiry = ?, suppliers = ? 
        WHERE ingre_id = ?
        """
        result = self.db.execute_query(
            query, (name, stock, unit, expiry, suppliers, ingre_id), commit=True
        )
        
        if result:
            logger.info(f"Updated ingredient ID {ingre_id}")
        return bool(result)
    
    def delete(self, ingre_id: int) -> bool:
        """Deletes an ingredient"""
        query = "DELETE FROM Ingredients WHERE ingre_id = ?"
        result = self.db.execute_query(query, (ingre_id,), commit=True)
        
        if result:
            logger.info(f"Deleted ingredient ID {ingre_id}")
        return bool(result)
    
    def get_low_stock(self, threshold: float = 10.0) -> List[sqlite3.Row]:
        """Gets ingredients with low stock"""
        query = """
        SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers 
        FROM Ingredients 
        WHERE stock < ?
        ORDER BY stock ASC
        """
        return self.db.execute_query(query, (threshold,)) or []
    
    def get_expired(self) -> List[sqlite3.Row]:
        """Gets expired ingredients"""
        today = datetime.date.today().isoformat()
        query = """
        SELECT ingre_id, ingre_name, stock, unit, expiry, suppliers 
        FROM Ingredients 
        WHERE expiry < ?
        ORDER BY expiry ASC
        """
        return self.db.execute_query(query, (today,)) or []


class ShipperManager:
    """Handles all shipper-related operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_all(self) -> List[sqlite3.Row]:
        """Retrieves all shippers"""
        query = "SELECT shipper_id, shipper_info FROM Shippers ORDER BY shipper_id"
        return self.db.execute_query(query) or []
    
    def get_by_id(self, shipper_id: int) -> Optional[sqlite3.Row]:
        """Finds shipper by ID"""
        query = "SELECT shipper_id, shipper_info FROM Shippers WHERE shipper_id = ?"
        return self.db.execute_query(query, (shipper_id,), fetch_one=True)


class OrderManager:
    """Handles order, bill, and delivery operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_order(
        self, dish_req_string: str, total_price: float, cus_id: int
    ) -> Optional[int]:
        """
        Creates a new order
        
        Returns:
            Order ID if successful, None otherwise
        """
        if not dish_req_string or total_price <= 0:
            logger.warning("Invalid order data")
            return None
        
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = OrderStatus.PENDING.value
        
        query = """
        INSERT INTO Orders (dish_req, total_price, order_time, status, cus_id) 
        VALUES (?, ?, ?, ?, ?)
        """
        order_id = self.db.execute_with_lastrowid(
            query, (dish_req_string, total_price, order_time, status, cus_id)
        )
        
        if order_id:
            logger.info(f"Created order ID {order_id} for customer {cus_id}")
        
        return order_id
    
    def create_bill(
        self, order_id: int, emp_id: int, shipper_id: int, total_amount: float
    ) -> bool:
        """Creates a bill for an order"""
        bill_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Bills (order_id, emp_id, shipper_id, total_amount, bill_time) 
        VALUES (?, ?, ?, ?, ?)
        """
        result = self.db.execute_query(
            query, (order_id, emp_id, shipper_id, total_amount, bill_time), commit=True
        )
        
        if result:
            logger.info(f"Created bill for order {order_id}")
        return bool(result)
    
    def add_delivery(
        self, order_id: int, shipper_id: int, delivery_addr: str, distance: float, fee: float
    ) -> bool:
        """Adds delivery information"""
        delivery_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO Deliveries (order_id, shipper_id, delivery_time, delivery_addr, distance, fee) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        result = self.db.execute_query(
            query, (order_id, shipper_id, delivery_time, delivery_addr, distance, fee), 
            commit=True
        )
        
        if result:
            logger.info(f"Added delivery for order {order_id}")
        return bool(result)
    
    def get_all_orders_details(self) -> List[sqlite3.Row]:
        """Retrieves all orders with customer details"""
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
        return self.db.execute_query(query) or []
    
    def get_order_by_id(self, order_id: int) -> Optional[sqlite3.Row]:
        """Gets detailed order information"""
        query = """
        SELECT 
            o.order_id, o.dish_req, o.total_price, o.order_time, o.status,
            c.cus_id, c.cus_name, c.cus_phone
        FROM 
            Orders o
        JOIN 
            Customers c ON o.cus_id = c.cus_id
        WHERE 
            o.order_id = ?
        """
        return self.db.execute_query(query, (order_id,), fetch_one=True)
    
    def update_status(self, order_id: int, status: str) -> bool:
        """Updates order status"""
        # Validate status
        try:
            OrderStatus(status)
        except ValueError:
            logger.warning(f"Invalid order status: {status}")
            return False
        
        query = "UPDATE Orders SET status = ? WHERE order_id = ?"
        result = self.db.execute_query(query, (status, order_id), commit=True)
        
        if result:
            logger.info(f"Updated order {order_id} status to {status}")
        return bool(result)
    
    def get_delivery_info(self, order_id: int) -> Optional[sqlite3.Row]:
        """Retrieves delivery details for an order"""
        query = """
        SELECT 
            d.delivery_addr, d.distance, d.fee, d.delivery_time,
            s.shipper_info
        FROM 
            Deliveries d
        JOIN 
            Shippers s ON d.shipper_id = s.shipper_id
        WHERE 
            d.order_id = ?
        """
        return self.db.execute_query(query, (order_id,), fetch_one=True)
    
    def get_orders_by_status(self, status: str) -> List[sqlite3.Row]:
        """Gets orders filtered by status"""
        query = """
        SELECT 
            o.order_id, o.dish_req, o.total_price, o.order_time, o.status,
            c.cus_name, c.cus_phone
        FROM 
            Orders o
        JOIN 
            Customers c ON o.cus_id = c.cus_id
        WHERE 
            o.status = ?
        ORDER BY 
            o.order_time DESC
        """
        return self.db.execute_query(query, (status,)) or []
    
    def get_revenue_report(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates revenue report for date range"""
        if not start_date:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_price) as total_revenue,
            AVG(total_price) as avg_order_value
        FROM Orders
        WHERE DATE(order_time) BETWEEN ? AND ?
        """
        result = self.db.execute_query(query, (start_date, end_date), fetch_one=True)
        
        if result:
            return {
                'start_date': start_date,
                'end_date': end_date,
                'total_orders': result['total_orders'] or 0,
                'total_revenue': result['total_revenue'] or 0.0,
                'avg_order_value': result['avg_order_value'] or 0.0
            }
        return {}


# --- Facade Class for Easy Access ---

class FoodManagementSystem:
    """Main facade class providing access to all managers"""
    
    def __init__(self, db_name: str = DATABASE_NAME):
        self.db_manager = DatabaseManager(db_name)
        self.customers = CustomerManager(self.db_manager)
        self.employees = EmployeeManager(self.db_manager)
        self.dishes = DishManager(self.db_manager)
        self.ingredients = IngredientManager(self.db_manager)
        self.shippers = ShipperManager(self.db_manager)
        self.orders = OrderManager(self.db_manager)
        
        logger.info("Food Management System initialized")
    
    def health_check(self) -> bool:
        """Checks if database is accessible"""
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


# --- Usage Example ---
if __name__ == "__main__":
    # Initialize system
    system = FoodManagementSystem()
    
    # Check system health
    if system.health_check():
        print("✓ System is operational")
    
    # Example operations
    # system.customers.add("John Doe", "555-1234")
    # system.dishes.add("Pasta Carbonara", "Classic Italian pasta", 25, 12.99)
    # all_customers = system.customers.get_all()
    # print(f"Total customers: {len(all_customers)}")