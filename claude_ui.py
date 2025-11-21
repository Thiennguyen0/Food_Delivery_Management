"""
Colorful, Interactive Food Management System GUI with Tkinter
Features: Modern design, animations, gradients, and smooth interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime, timedelta
import random

# Import the backend (assuming it's in the same directory)
try:
    from claude_logic import FoodManagementSystem, OrderStatus
except ImportError:
    print("Warning: Backend module not found. Running in demo mode.")
    FoodManagementSystem = None

class ModernButton(tk.Canvas):
    """Custom animated button with gradient and hover effects"""
    def __init__(self, parent, text, command, bg_color="#4CAF50", hover_color="#45a049", **kwargs):
        super().__init__(parent, height=40, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        self.is_hovered = False
        
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self):
        self.delete("all")
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw rounded rectangle
        x1, y1, x2, y2 = 5, 5, self.winfo_reqwidth() - 5, 35
        r = 15
        self.create_arc(x1, y1, x1+r, y1+r, start=90, extent=90, fill=color, outline=color)
        self.create_arc(x2-r, y1, x2, y1+r, start=0, extent=90, fill=color, outline=color)
        self.create_arc(x1, y2-r, x1+r, y2, start=180, extent=90, fill=color, outline=color)
        self.create_arc(x2-r, y2-r, x2, y2, start=270, extent=90, fill=color, outline=color)
        self.create_rectangle(x1+r/2, y1, x2-r/2, y2, fill=color, outline=color)
        self.create_rectangle(x1, y1+r/2, x2, y2-r/2, fill=color, outline=color)
        
        # Add text
        self.create_text(self.winfo_reqwidth()//2, 20, text=self.text, 
                        fill="white", font=("Segoe UI", 10, "bold"))
    
    def on_enter(self, e):
        self.is_hovered = True
        self.draw_button()
    
    def on_leave(self, e):
        self.is_hovered = False
        self.draw_button()
    
    def on_click(self, e):
        self.animate_click()
        if self.command:
            self.command()
    
    def animate_click(self):
        original_color = self.bg_color
        self.bg_color = "#333333"
        self.draw_button()
        self.after(100, lambda: setattr(self, 'bg_color', original_color) or self.draw_button())


class AnimatedCard(tk.Frame):
    """Animated card widget with shadow effect"""
    def __init__(self, parent, title, value, icon, color, **kwargs):
        super().__init__(parent, bg="#ffffff", relief="flat", **kwargs)
        self.color = color
        self.lifted = False
        
        # Border frame for shadow effect
        self.border = tk.Frame(self, bg="#e0e0e0", padx=2, pady=2)
        self.border.pack(fill="both", expand=True)
        
        # Main content frame
        content = tk.Frame(self.border, bg="#ffffff")
        content.pack(fill="both", expand=True)
        
        # Icon and title
        header = tk.Frame(content, bg="#ffffff")
        header.pack(fill="x", padx=20, pady=(15, 5))
        
        icon_label = tk.Label(header, text=icon, font=("Segoe UI Emoji", 24), 
                             bg="#ffffff", fg=color)
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = tk.Label(header, text=title, font=("Segoe UI", 11), 
                              bg="#ffffff", fg="#666666")
        title_label.pack(side="left", anchor="w")
        
        # Value
        self.value_label = tk.Label(content, text=value, font=("Segoe UI", 28, "bold"),
                                    bg="#ffffff", fg=color)
        self.value_label.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Hover effects
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        for widget in [content, header, icon_label, title_label, self.value_label]:
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        if not self.lifted:
            self.lifted = True
            self.border.configure(bg=self.color, padx=3, pady=3)
    
    def on_leave(self, e):
        if self.lifted:
            self.lifted = False
            self.border.configure(bg="#e0e0e0", padx=2, pady=2)
    
    def update_value(self, new_value):
        self.value_label.configure(text=new_value)


class FoodManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Food Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f5f5f5")
        
        # Initialize backend
        if FoodManagementSystem:
            self.system = FoodManagementSystem()
        else:
            self.system = None
        
        # Color scheme
        self.colors = {
            'primary': '#FF6B6B',
            'secondary': '#4ECDC4',
            'success': '#95E1D3',
            'warning': '#F38181',
            'info': '#AA96DA',
            'dark': '#2C3E50',
            'light': '#ECF0F1'
        }
        
        # Setup UI
        self.setup_styles()
        self.create_sidebar()
        self.create_main_content()
        self.show_dashboard()
        
        # Start animation loop
        self.animate_cards()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       rowheight=35,
                       fieldbackground="white",
                       font=("Segoe UI", 10))
        style.map('Treeview', background=[('selected', self.colors['secondary'])])
        
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))
        
        # Configure Entry
        style.configure("TEntry", fieldbackground="white", font=("Segoe UI", 10))
        
        # Configure Combobox
        style.configure("TCombobox", fieldbackground="white", font=("Segoe UI", 10))
    
    def create_sidebar(self):
        """Create animated sidebar with navigation"""
        self.sidebar = tk.Frame(self.root, bg=self.colors['dark'], width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo/Title with gradient effect
        title_frame = tk.Frame(self.sidebar, bg=self.colors['primary'], height=100)
        title_frame.pack(fill="x", pady=(0, 30))
        
        logo = tk.Label(title_frame, text="🍽️", font=("Segoe UI Emoji", 40),
                       bg=self.colors['primary'], fg="white")
        logo.pack(pady=(20, 5))
        
        title = tk.Label(title_frame, text="Food Manager", 
                        font=("Segoe UI", 16, "bold"),
                        bg=self.colors['primary'], fg="white")
        title.pack()
        
        # Navigation buttons
        nav_items = [
            ("📊 Dashboard", "dashboard", self.colors['info']),
            ("👥 Customers", "customers", self.colors['secondary']),
            ("🍕 Dishes", "dishes", self.colors['warning']),
            ("📦 Ingredients", "ingredients", self.colors['success']),
            ("🛒 Orders", "orders", self.colors['primary']),
            ("👨‍🍳 Employees", "employees", self.colors['info']),
        ]
        
        self.nav_buttons = {}
        for text, key, color in nav_items:
            btn_frame = tk.Frame(self.sidebar, bg=self.colors['dark'])
            btn_frame.pack(fill="x", padx=15, pady=5)
            
            btn = tk.Button(btn_frame, text=text, font=("Segoe UI", 12, "bold"),
                          bg=self.colors['dark'], fg="white", 
                          activebackground=color, activeforeground="white",
                          relief="flat", anchor="w", padx=20, pady=12,
                          command=lambda k=key: self.switch_view(k))
            btn.pack(fill="x")
            self.nav_buttons[key] = btn
        
        # Footer
        footer = tk.Label(self.sidebar, text="v2.0 - Premium Edition",
                         font=("Segoe UI", 8), bg=self.colors['dark'], fg="#7f8c8d")
        footer.pack(side="bottom", pady=20)
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.main_frame.pack(side="right", fill="both", expand=True)
    
    def clear_main_frame(self):
        """Clear main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def switch_view(self, view):
        """Switch between different views with animation"""
        # Highlight active button
        for key, btn in self.nav_buttons.items():
            if key == view:
                btn.configure(bg=self.colors['primary'])
            else:
                btn.configure(bg=self.colors['dark'])
        
        # Fade out animation (simple version)
        self.clear_main_frame()
        
        # Show selected view
        if view == "dashboard":
            self.show_dashboard()
        elif view == "customers":
            self.show_customers()
        elif view == "dishes":
            self.show_dishes()
        elif view == "ingredients":
            self.show_ingredients()
        elif view == "orders":
            self.show_orders()
        elif view == "employees":
            self.show_employees()
    
    def show_dashboard(self):
        """Display dashboard with statistics and charts"""
        # Header
        header = tk.Frame(self.main_frame, bg="#f5f5f5")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        title = tk.Label(header, text="Dashboard Overview", 
                        font=("Segoe UI", 28, "bold"),
                        bg="#f5f5f5", fg=self.colors['dark'])
        title.pack(side="left")
        
        date_label = tk.Label(header, 
                             text=datetime.now().strftime("%B %d, %Y"),
                             font=("Segoe UI", 12),
                             bg="#f5f5f5", fg="#7f8c8d")
        date_label.pack(side="right", pady=(10, 0))
        
        # Stats cards
        stats_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        stats_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Get actual data if backend available
        total_orders = len(self.system.orders.get_all_orders_details()) if self.system else 0
        total_customers = len(self.system.customers.get_all()) if self.system else 0
        total_dishes = len(self.system.dishes.get_all()) if self.system else 0
        
        # Calculate revenue
        revenue = 0
        if self.system:
            orders = self.system.orders.get_all_orders_details()
            revenue = sum(order['total_price'] for order in orders)
        
        self.stat_cards = []
        stats_data = [
            ("Total Revenue", f"${revenue:,.2f}", "💰", self.colors['success']),
            ("Orders Today", str(total_orders), "🛒", self.colors['warning']),
            ("Active Customers", str(total_customers), "👥", self.colors['secondary']),
            ("Menu Items", str(total_dishes), "🍕", self.colors['info'])
        ]
        
        for i, (title, value, icon, color) in enumerate(stats_data):
            card = AnimatedCard(stats_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)
            self.stat_cards.append(card)
        
        # Recent activity section
        activity_frame = tk.Frame(self.main_frame, bg="white", relief="flat")
        activity_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Border for shadow
        border = tk.Frame(activity_frame, bg="#e0e0e0", padx=2, pady=2)
        border.pack(fill="both", expand=True)
        
        content = tk.Frame(border, bg="white")
        content.pack(fill="both", expand=True)
        
        # Activity header
        act_header = tk.Frame(content, bg="white")
        act_header.pack(fill="x", padx=20, pady=20)
        
        tk.Label(act_header, text="📈 Recent Activity", 
                font=("Segoe UI", 18, "bold"),
                bg="white", fg=self.colors['dark']).pack(side="left")
        
        # Quick action buttons
        quick_actions = tk.Frame(content, bg="white")
        quick_actions.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_new_order = ModernButton(quick_actions, "➕ New Order", 
                                     self.new_order_dialog,
                                     bg_color=self.colors['primary'],
                                     hover_color=self.colors['warning'],
                                     width=150)
        btn_new_order.pack(side="left", padx=(0, 10))
        
        btn_add_customer = ModernButton(quick_actions, "👤 Add Customer",
                                       self.add_customer_dialog,
                                       bg_color=self.colors['secondary'],
                                       hover_color=self.colors['info'],
                                       width=150)
        btn_add_customer.pack(side="left", padx=(0, 10))
        
        btn_inventory = ModernButton(quick_actions, "📦 Check Stock",
                                    lambda: self.switch_view('ingredients'),
                                    bg_color=self.colors['success'],
                                    hover_color=self.colors['secondary'],
                                    width=150)
        btn_inventory.pack(side="left")
        
        # Recent orders table
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("ID", "Customer", "Items", "Amount", "Status", "Time")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load recent orders
        if self.system:
            orders = self.system.orders.get_all_orders_details()
            for order in orders[:10]:  # Show last 10 orders
                tree.insert("", "end", values=(
                    order['order_id'],
                    order['cus_name'],
                    order['dish_req'][:30] + "..." if len(order['dish_req']) > 30 else order['dish_req'],
                    f"${order['total_price']:.2f}",
                    order['status'],
                    order['order_time']
                ))
    
    def show_customers(self):
        """Display customers management view"""
        self.create_crud_view(
            title="👥 Customer Management",
            columns=("ID", "Name", "Phone"),
            data_source=lambda: self.system.customers.get_all() if self.system else [],
            add_callback=self.add_customer_dialog,
            edit_callback=self.edit_customer_dialog,
            delete_callback=self.delete_customer,
            color=self.colors['secondary']
        )
    
    def show_dishes(self):
        """Display dishes management view"""
        self.create_crud_view(
            title="🍕 Dish Management",
            columns=("ID", "Name", "Recipe", "Time (min)", "Price"),
            data_source=lambda: self.system.dishes.get_all() if self.system else [],
            add_callback=self.add_dish_dialog,
            edit_callback=self.edit_dish_dialog,
            delete_callback=self.delete_dish,
            color=self.colors['warning']
        )
    
    def show_ingredients(self):
        """Display ingredients management view"""
        self.create_crud_view(
            title="📦 Ingredient Inventory",
            columns=("ID", "Name", "Stock", "Unit", "Expiry", "Supplier"),
            data_source=lambda: self.system.ingredients.get_all() if self.system else [],
            add_callback=self.add_ingredient_dialog,
            edit_callback=self.edit_ingredient_dialog,
            delete_callback=self.delete_ingredient,
            color=self.colors['success'],
            highlight_callback=self.highlight_low_stock
        )
    
    def show_orders(self):
        """Display orders management view"""
        self.create_crud_view(
            title="🛒 Order Management",
            columns=("ID", "Customer", "Items", "Amount", "Status", "Time"),
            data_source=lambda: self.system.orders.get_all_orders_details() if self.system else [],
            add_callback=self.new_order_dialog,
            edit_callback=self.edit_order_dialog,
            delete_callback=None,
            color=self.colors['primary']
        )
    
    def show_employees(self):
        """Display employees management view"""
        self.create_crud_view(
            title="👨‍🍳 Employee Management",
            columns=("ID", "Name"),
            data_source=lambda: self.system.employees.get_all() if self.system else [],
            add_callback=self.add_employee_dialog,
            edit_callback=self.edit_employee_dialog,
            delete_callback=self.delete_employee,
            color=self.colors['info']
        )
    
    def create_crud_view(self, title, columns, data_source, add_callback, 
                        edit_callback, delete_callback, color, highlight_callback=None):
        """Generic CRUD view creator"""
        # Header
        header = tk.Frame(self.main_frame, bg="#f5f5f5")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        tk.Label(header, text=title, font=("Segoe UI", 28, "bold"),
                bg="#f5f5f5", fg=self.colors['dark']).pack(side="left")
        
        # Toolbar
        toolbar = tk.Frame(self.main_frame, bg="white", relief="flat")
        toolbar.pack(fill="x", padx=30, pady=(0, 10))
        
        border = tk.Frame(toolbar, bg="#e0e0e0", padx=2, pady=2)
        border.pack(fill="both", expand=True)
        
        tool_content = tk.Frame(border, bg="white")
        tool_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Search
        search_frame = tk.Frame(tool_content, bg="white")
        search_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(search_frame, text="🔍", font=("Segoe UI Emoji", 14),
                bg="white").pack(side="left", padx=(0, 5))
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                               font=("Segoe UI", 11), relief="flat",
                               bg="#f8f9fa", width=30)
        search_entry.pack(side="left", ipady=8, padx=(0, 10))
        
        # Action buttons
        btn_add = ModernButton(tool_content, "➕ Add New", add_callback,
                              bg_color=color, width=120)
        btn_add.pack(side="right", padx=(10, 0))
        
        if edit_callback:
            btn_edit = ModernButton(tool_content, "✏️ Edit", 
                                   lambda: edit_callback(tree),
                                   bg_color=self.colors['info'], width=100)
            btn_edit.pack(side="right", padx=(10, 0))
        
        if delete_callback:
            btn_delete = ModernButton(tool_content, "🗑️ Delete",
                                     lambda: delete_callback(tree),
                                     bg_color=self.colors['warning'], width=100)
            btn_delete.pack(side="right")
        
        # Data table
        table_frame = tk.Frame(self.main_frame, bg="white", relief="flat")
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        border2 = tk.Frame(table_frame, bg="#e0e0e0", padx=2, pady=2)
        border2.pack(fill="both", expand=True)
        
        content = tk.Frame(border2, bg="white")
        content.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(content, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
        
        # Load data
        self.refresh_table(tree, data_source, highlight_callback)
        
        # Search functionality
        def on_search(*args):
            search_text = search_var.get().lower()
            for item in tree.get_children():
                tree.delete(item)
            
            data = data_source()
            for row in data:
                row_values = tuple(row[col] if col in row.keys() else "" for col in columns)
                if search_text in str(row_values).lower():
                    tree.insert("", "end", values=row_values)
        
        search_var.trace("w", on_search)
    
    def refresh_table(self, tree, data_source, highlight_callback=None):
        """Refresh table data"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = data_source()
        for row in data:
            values = tuple(row[col] if col in row.keys() else "" for col in tree["columns"])
            item_id = tree.insert("", "end", values=values)
            
            if highlight_callback:
                highlight_callback(tree, item_id, row)
    
    def highlight_low_stock(self, tree, item_id, row):
        """Highlight low stock items"""
        if row['stock'] < 10:
            tree.item(item_id, tags=('low_stock',))
            tree.tag_configure('low_stock', background='#ffe6e6')
    
    # Dialog methods
    def add_customer_dialog(self):
        self.show_form_dialog("Add Customer", [
            ("Name:", "name"),
            ("Phone:", "phone")
        ], self.save_customer)
    
    def add_dish_dialog(self):
        self.show_form_dialog("Add Dish", [
            ("Name:", "name"),
            ("Recipe:", "recipe"),
            ("Cooking Time (min):", "time"),
            ("Price ($):", "price")
        ], self.save_dish)
    
    def add_ingredient_dialog(self):
        self.show_form_dialog("Add Ingredient", [
            ("Name:", "name"),
            ("Stock:", "stock"),
            ("Unit:", "unit"),
            ("Expiry (YYYY-MM-DD):", "expiry"),
            ("Supplier:", "supplier")
        ], self.save_ingredient)
    
    def add_employee_dialog(self):
        self.show_form_dialog("Add Employee", [
            ("Name:", "name")
        ], self.save_employee)
    
    def new_order_dialog(self):
        """Create new order dialog"""
        if not self.system:
            messagebox.showwarning("Demo Mode", "Backend not available")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("New Order")
        dialog.geometry("600x500")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=80)
        header.pack(fill="x")
        
        tk.Label(header, text="🛒 New Order", font=("Segoe UI", 20, "bold"),
                bg=self.colors['primary'], fg="white").pack(pady=25)
        
        # Form
        form = tk.Frame(dialog, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Customer selection
        tk.Label(form, text="Customer:", font=("Segoe UI", 11, "bold"),
                bg="white").grid(row=0, column=0, sticky="w", pady=10)
        
        customers = self.system.customers.get_all()
        customer_names = [f"{c['cus_name']} ({c['cus_phone']})" for c in customers]
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(form, textvariable=customer_var,
                                     values=customer_names, state="readonly",
                                     font=("Segoe UI", 10), width=40)
        customer_combo.grid(row=0, column=1, pady=10, sticky="ew")
        
        # Dishes selection
        tk.Label(form, text="Dishes:", font=("Segoe UI", 11, "bold"),
                bg="white").grid(row=1, column=0, sticky="nw", pady=10)
        
        dishes_frame = tk.Frame(form, bg="white")
        dishes_frame.grid(row=1, column=1, pady=10, sticky="ew")
        
        dishes = self.system.dishes.get_all()
        dish_vars = []
        total_var = tk.DoubleVar(value=0.0)
        
        def update_total():
            total = sum(dish['dish_price'] * var.get() 
                       for dish, var in zip(dishes, dish_vars))
            total_var.set(total)
            total_label.configure(text=f"${total:.2f}")
        
        for dish in dishes:
            dish_row = tk.Frame(dishes_frame, bg="white")
            dish_row.pack(fill="x", pady=2)
            
            var = tk.IntVar(value=0)
            dish_vars.append(var)
            
            tk.Checkbutton(dish_row, text=f"{dish['dish_name']} - ${dish['dish_price']:.2f}",
                          variable=var, bg="white", font=("Segoe UI", 10),
                          command=update_total).pack(side="left")
        
        # Total
        total_frame = tk.Frame(form, bg=self.colors['light'])
        total_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)
        
        tk.Label(total_frame, text="Total Amount:", font=("Segoe UI", 12, "bold"),
                bg=self.colors['light']).pack(side="left", padx=20, pady=15)
        
        total_label = tk.Label(total_frame, text="$0.00",
                              font=("Segoe UI", 18, "bold"),
                              bg=self.colors['light'], fg=self.colors['primary'])
        total_label.pack(side="right", padx=20)
        
        form.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        def save_order():
            if not customer_var.get():
                messagebox.showerror("Error", "Please select a customer")
                return
            
            selected_dishes = []
            for dish, var in zip(dishes, dish_vars):
                if var.get():
                    selected_dishes.append(dish['dish_name'])
            
            if not selected_dishes:
                messagebox.showerror("Error", "Please select at least one dish")
                return
            
            # Get customer ID
            cus_name = customer_var.get().split(" (")[0]
            customer = self.system.customers.get_by_phone(
                customer_var.get().split("(")[1].replace(")", "")
            )
            
            # Create order
            dish_req = ", ".join(selected_dishes)
            order_id = self.system.orders.create_order(
                dish_req, total_var.get(), customer['cus_id']
            )
            
            if order_id:
                messagebox.showinfo("Success", f"Order #{order_id} created successfully!")
                dialog.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Failed to create order")
        
        btn_save = ModernButton(btn_frame, "💾 Create Order", save_order,
                               bg_color=self.colors['primary'], width=150)
        btn_save.pack(side="right", padx=(10, 0))
        
        btn_cancel = ModernButton(btn_frame, "✖ Cancel", dialog.destroy,
                                 bg_color="#95a5a6", width=150)
        btn_cancel.pack(side="right")
    
    def show_form_dialog(self, title, fields, save_callback):
        """Generic form dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Header with gradient effect
        header = tk.Frame(dialog, bg=self.colors['secondary'], height=80)
        header.pack(fill="x")
        
        tk.Label(header, text=title, font=("Segoe UI", 20, "bold"),
                bg=self.colors['secondary'], fg="white").pack(pady=25)
        
        # Form
        form = tk.Frame(dialog, bg="white")
        form.pack(fill="both", expand=True, padx=40, pady=30)
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, font=("Segoe UI", 11, "bold"),
                    bg="white").grid(row=i, column=0, sticky="w", pady=10)
            
            entry = tk.Entry(form, font=("Segoe UI", 11), relief="solid",
                           borderwidth=1, width=30)
            entry.grid(row=i, column=1, pady=10, padx=(10, 0), sticky="ew")
            entries[key] = entry
        
        form.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        def save():
            data = {key: entry.get() for key, entry in entries.items()}
            if save_callback(data):
                dialog.destroy()
        
        btn_save = ModernButton(btn_frame, "💾 Save", save,
                               bg_color=self.colors['success'], width=120)
        btn_save.pack(side="right", padx=(10, 0))
        
        btn_cancel = ModernButton(btn_frame, "✖ Cancel", dialog.destroy,
                                 bg_color="#95a5a6", width=120)
        btn_cancel.pack(side="right")
    
    # Save callbacks
    def save_customer(self, data):
        if not self.system:
            messagebox.showwarning("Demo Mode", "Backend not available")
            return False
        
        if not data['name'] or not data['phone']:
            messagebox.showerror("Error", "All fields are required")
            return False
        
        if self.system.customers.add(data['name'], data['phone']):
            messagebox.showinfo("Success", "Customer added successfully!")
            self.show_customers()
            return True
        else:
            messagebox.showerror("Error", "Failed to add customer")
            return False
    
    def save_dish(self, data):
        if not self.system:
            messagebox.showwarning("Demo Mode", "Backend not available")
            return False
        
        try:
            cooking_time = int(data['time'])
            price = float(data['price'])
        except ValueError:
            messagebox.showerror("Error", "Invalid time or price")
            return False
        
        if self.system.dishes.add(data['name'], data['recipe'], cooking_time, price):
            messagebox.showinfo("Success", "Dish added successfully!")
            self.show_dishes()
            return True
        else:
            messagebox.showerror("Error", "Failed to add dish")
            return False
    
    def save_ingredient(self, data):
        if not self.system:
            messagebox.showwarning("Demo Mode", "Backend not available")
            return False
        
        try:
            stock = float(data['stock'])
        except ValueError:
            messagebox.showerror("Error", "Invalid stock amount")
            return False
        
        if self.system.ingredients.add(data['name'], stock, data['unit'], 
                                       data['expiry'], data['supplier']):
            messagebox.showinfo("Success", "Ingredient added successfully!")
            self.show_ingredients()
            return True
        else:
            messagebox.showerror("Error", "Failed to add ingredient")
            return False
    
    def save_employee(self, data):
        if not self.system:
            messagebox.showwarning("Demo Mode", "Backend not available")
            return False
        
        if self.system.employees.add(data['name']):
            messagebox.showinfo("Success", "Employee added successfully!")
            self.show_employees()
            return True
        else:
            messagebox.showerror("Error", "Failed to add employee")
            return False
    
    # Edit callbacks
    def edit_customer_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return
        
        values = tree.item(selected[0])['values']
        # Implementation similar to add but with pre-filled values
        messagebox.showinfo("Edit", f"Editing customer: {values[1]}")
    
    def edit_dish_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a dish to edit")
            return
        
        values = tree.item(selected[0])['values']
        messagebox.showinfo("Edit", f"Editing dish: {values[1]}")
    
    def edit_ingredient_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an ingredient to edit")
            return
        
        values = tree.item(selected[0])['values']
        messagebox.showinfo("Edit", f"Editing ingredient: {values[1]}")
    
    def edit_employee_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return
        
        values = tree.item(selected[0])['values']
        messagebox.showinfo("Edit", f"Editing employee: {values[1]}")
    
    def edit_order_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to edit")
            return
        
        values = tree.item(selected[0])['values']
        order_id = values[0]
        
        # Status update dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Order Status")
        dialog.geometry("400x300")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=70)
        header.pack(fill="x")
        
        tk.Label(header, text=f"Update Order #{order_id}", 
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['primary'], fg="white").pack(pady=20)
        
        # Status selection
        form = tk.Frame(dialog, bg="white")
        form.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(form, text="New Status:", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)
        
        status_var = tk.StringVar(value="Pending")
        statuses = ["Pending", "Preparing", "Ready", "Delivered", "Cancelled"]
        
        for status in statuses:
            rb = tk.Radiobutton(form, text=status, variable=status_var,
                               value=status, font=("Segoe UI", 11),
                               bg="white")
            rb.pack(anchor="w", pady=5)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        def update_status():
            if self.system:
                if self.system.orders.update_status(order_id, status_var.get()):
                    messagebox.showinfo("Success", "Order status updated!")
                    dialog.destroy()
                    self.show_orders()
                else:
                    messagebox.showerror("Error", "Failed to update status")
            else:
                messagebox.showwarning("Demo Mode", "Backend not available")
        
        btn_update = ModernButton(btn_frame, "✔ Update", update_status,
                                 bg_color=self.colors['success'], width=120)
        btn_update.pack(side="right", padx=(10, 0))
        
        btn_cancel = ModernButton(btn_frame, "✖ Cancel", dialog.destroy,
                                 bg_color="#95a5a6", width=120)
        btn_cancel.pack(side="right")
    
    # Delete callbacks
    def delete_customer(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        values = tree.item(selected[0])['values']
        cus_id = values[0]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete {values[1]}?"):
            if self.system and self.system.customers.delete(cus_id):
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.show_customers()
            else:
                messagebox.showerror("Error", "Failed to delete customer")
    
    def delete_dish(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a dish to delete")
            return
        
        values = tree.item(selected[0])['values']
        dish_id = values[0]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete {values[1]}?"):
            if self.system and self.system.dishes.delete(dish_id):
                messagebox.showinfo("Success", "Dish deleted successfully!")
                self.show_dishes()
            else:
                messagebox.showerror("Error", "Failed to delete dish")
    
    def delete_ingredient(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an ingredient to delete")
            return
        
        values = tree.item(selected[0])['values']
        ingre_id = values[0]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete {values[1]}?"):
            if self.system and self.system.ingredients.delete(ingre_id):
                messagebox.showinfo("Success", "Ingredient deleted successfully!")
                self.show_ingredients()
            else:
                messagebox.showerror("Error", "Failed to delete ingredient")
    
    def delete_employee(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        values = tree.item(selected[0])['values']
        emp_id = values[0]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete {values[1]}?"):
            if self.system and self.system.employees.delete(emp_id):
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.show_employees()
            else:
                messagebox.showerror("Error", "Failed to delete employee")
    
    def animate_cards(self):
        """Animate dashboard cards with random updates"""
        if hasattr(self, 'stat_cards') and self.stat_cards:
            # Simulate live updates (for demo purposes)
            if random.random() > 0.7:  # 30% chance to update
                card_idx = random.randint(0, len(self.stat_cards) - 1)
                card = self.stat_cards[card_idx]
                
                # Add small random change to value
                current_text = card.value_label.cget("text")
                if "$" in current_text:
                    try:
                        value = float(current_text.replace("$", "").replace(",", ""))
                        change = random.uniform(-10, 20)
                        new_value = value + change
                        card.update_value(f"${new_value:,.2f}")
                    except:
                        pass
        
        # Schedule next animation
        self.root.after(3000, self.animate_cards)


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set app icon and styling
    try:
        root.iconbitmap("icon.ico")  # Optional: Add your icon
    except:
        pass
    
    app = FoodManagementGUI(root)
    
    # Smooth startup animation
    root.attributes('-alpha', 0.0)
    root.update()
    
    def fade_in(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.1
            root.attributes('-alpha', alpha)
            root.after(30, lambda: fade_in(alpha))
    
    fade_in()
    
    root.mainloop()


if __name__ == "__main__":
    main()