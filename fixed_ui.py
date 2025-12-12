import customtkinter
import backend

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# global functions

def on_enter(event, frame, color):
    frame.configure(border_color=color)

def on_leave(event, frame, color):
    frame.configure(border_color=color)


def show_frame(root, sframe):
    for button in root.SelectionBar.winfo_children()[1:]:
        if button.cget("text") == sframe.__name__ and (button.cget('fg_color') != '#1f538d' or button.cget("font") != ('Arial', 24, 'bold')):
            # Fixed: Use getattr instead of eval for safety
            getattr(root.SelectionBar, sframe.__name__).configure(fg_color='#1f538d', font=('Arial', 24, 'bold'))
        elif button.cget("text") != sframe.__name__:
            # Fixed: Use getattr instead of eval
            getattr(root.SelectionBar, button.cget('text')).configure(fg_color=['gray90', 'gray15'], font=('Arial', 24))

    for frame in root.winfo_children()[1:]:
        if isinstance(frame, sframe):
            frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        else:
            frame.grid_forget()



#Class definition

class Selection_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.Label = customtkinter.CTkLabel(self, text="Food Delivery\nManagement", font=("Arial", 50, "bold"), pady=25)
        self.Label.grid(row = 0, column = 0, padx = 20, pady=20, sticky="nsew")

        self.Dashboard = customtkinter.CTkButton(self, text="Dashboard", font=("Arial", 24), command=self.Afunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Dashboard.grid(row = 1, column = 0, padx = 10, pady=(0, 20), sticky="ew")

        self.Customers = customtkinter.CTkButton(self, text="Customers", font=("Arial", 24), command=self.Bfunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Customers.grid(row = 2, column = 0, padx = 10, pady=(0, 20), sticky="ew")

        self.Dishes = customtkinter.CTkButton(self, text="Dishes", font=("Arial", 24), command=self.Cfunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Dishes.grid(row = 3, column = 0, padx = 10, pady=(0, 20), sticky="ew")

        self.Ingredients = customtkinter.CTkButton(self, text="Ingredients", font=("Arial", 24), command=self.Dfunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Ingredients.grid(row = 4, column = 0, padx = 10, pady=(0, 20), sticky="ew")

        self.Orders = customtkinter.CTkButton(self, text="Orders", font=("Arial", 24), command=self.Efunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Orders.grid(row = 5, column = 0, padx = 10, pady=(0, 20), sticky="ew")

        self.Employees = customtkinter.CTkButton(self, text="Employees", font=("Arial", 24), command=self.Ffunc, height=70, corner_radius=18, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Employees.grid(row = 6, column = 0, padx = 10, pady=(0, 20), sticky="ew")

    def Afunc(self): show_frame(self.master, Dashboard)
    def Bfunc(self): show_frame(self.master, Customers)
    def Cfunc(self): show_frame(self.master, Dishes)
    def Dfunc(self): show_frame(self.master, Ingredients)
    def Efunc(self): show_frame(self.master, Orders)
    def Ffunc(self): show_frame(self.master, Employees)

# --- 

class Dashboard(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.colors = {
            'revenue1': '#95E1D3',
            'order1': '#FF6B6B',
            'order2': '#F38181',
            'revenue2': "#00FF59",
            'leave': 'gray28',
            'info': '#AA96DA',
            'dark': '#2C3E50',
        }
        # print(self.cget('fg_color'))
        self.contentfont = ("Segoe UI", 24, 'bold')
        self.numberfont = ("Segoe UI", 34, 'bold')

        self.columnconfigure(0, weight=1)

        #Title
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0,column=0,padx=20, pady=10, sticky="nsw")
        self.label = customtkinter.CTkLabel(self.lbf, text="Dashboard Overview", text_color="#D8D8D8", font=('Segoe UI', 50, 'bold'))
        self.label.pack(padx=20,pady=20)


        #Maincontent------
        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=1, column=0,padx=20, pady=(0,20),sticky="nsew")
        self.contentf.columnconfigure(1, weight=1)
        self.contentf.columnconfigure(2, weight=1)
        self.contentf.columnconfigure(3, weight=1)
        self.contentf.columnconfigure(0, weight=1)

        order_rawdat = master.system.order_manager.get_all_orders_details()
        order_dat = [dict(order) for order in order_rawdat] if order_rawdat else []

        #Revenue
        self.revenuef = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.revenuef.grid(row=1,column=0,padx=20,pady=15, sticky="nsew")
        self.revenuef.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))
        self.revenuef.bind("<Leave>", lambda event2: on_leave(event2, self.revenuef,self.colors['leave']))

        self.revenuet = customtkinter.CTkLabel(self.revenuef, text=f"💰Total Revenue", text_color=self.colors['revenue1'], font=self.contentfont, anchor='center')

        total_revenue = sum(order['total_price'] for order in order_dat) if order_dat else 0
        self.revenue = customtkinter.CTkLabel(self.revenuef, text=f"{total_revenue:,.0f}", text_color=self.colors['revenue1'], font=self.numberfont, anchor='center')
        self.revenuet.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))
        self.revenue.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))
        self.revenuet.bind("<Leave>", lambda event2: on_leave(event2, self.revenuef,self.colors['leave']))
        self.revenue.bind("<Leave>", lambda event2: on_leave(event2, self.revenuef,self.colors['leave']))

        self.revenuet.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        self.revenue.grid(row=1,column=0,padx=25,pady=(0,25),sticky="nsew")

        #Order
        self.orderf = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.orderf.grid(row=1,column=1,padx=20,pady=15, sticky="nsew")
        self.orderf.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.orderf.bind("<Leave>", lambda event2: on_leave(event2, self.orderf, self.colors['leave']))

        self.ordert = customtkinter.CTkLabel(self.orderf, text=f"🛒Orders ", text_color=self.colors['order1'], font=self.contentfont)

        self.order = customtkinter.CTkLabel(self.orderf, text=f"{len(order_dat)}", text_color=self.colors['order1'], font=self.numberfont)
        self.ordert.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.order.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.ordert.bind("<Leave>", lambda event2: on_leave(event2, self.orderf,self.colors['leave']))
        self.order.bind("<Leave>", lambda event2: on_leave(event2, self.orderf,self.colors['leave']))

        self.ordert.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        # Fixed: stick -> sticky
        self.order.grid(row=1,column=0,padx=25,pady=(0,25),sticky="nsew")

        # Customers
        self.customersf = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.customersf.grid(row=1,column=2,padx=20,pady=15, sticky="nsew")
        self.customersf.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customersf.bind("<Leave>", lambda event2: on_leave(event2, self.customersf, self.colors['leave']))

        self.customerst = customtkinter.CTkLabel(self.customersf, text=f"👥Customers ", text_color=self.colors['info'], font=self.contentfont)

        cus_list = master.system.cus_manager.list_cus()
        cus_count = len(cus_list) if cus_list else 0
        self.customers = customtkinter.CTkLabel(self.customersf, text=f"{cus_count}", text_color=self.colors['info'], font=self.numberfont)
        self.customerst.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customers.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customerst.bind("<Leave>", lambda event2: on_leave(event2, self.customersf, self.colors['leave']))
        self.customers.bind("<Leave>", lambda event2: on_leave(event2, self.customersf, self.colors['leave']))

        self.customerst.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        # Fixed: stick -> sticky
        self.customers.grid(row=1,column=0,padx=25,pady=(0,25),sticky="nsew")

        #Menu Items
        self.menuitems = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.menuitems.grid(row=1,column=3,padx=20,pady=15, sticky="nsew")
        self.menuitems.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menuitems.bind("<Leave>", lambda event2: on_leave(event2, self.menuitems, self.colors['leave']))

        self.menut = customtkinter.CTkLabel(self.menuitems, text=f"🍕Menu Items ", text_color=self.colors['order2'], font=self.contentfont)

        dish_list = master.system.dish_manager.list_dishes()
        dish_count = len(dish_list) if dish_list else 0
        self.menu = customtkinter.CTkLabel(self.menuitems, text=f"{dish_count}", text_color=self.colors['order2'], font=self.numberfont)
        self.menut.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menu.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menut.bind("<Leave>", lambda event2: on_leave(event2, self.menuitems, self.colors['leave']))
        self.menu.bind("<Leave>", lambda event2: on_leave(event2, self.menuitems, self.colors['leave']))

        self.menut.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        # Fixed: stick -> sticky
        self.menu.grid(row=1,column=0,padx=25,pady=(0,25),sticky="nsew")
        
class Customers(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Header Frame
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.label = customtkinter.CTkLabel(
            self.lbf, text="Customer Management", text_color="#D8D8D8",
            font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)

        # Search Frame
        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')
        self.searchvar = customtkinter.StringVar()
        self.icon = customtkinter.CTkLabel(self.searchf, text="🔍", font=("Segoe UI Emoji", 24))
        self.icon.pack(side="left", padx=8, pady=10)
        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar, placeholder_text='Search for customers',
            fg_color=['gray90', 'gray16'], border_width=1, width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)
        self.searchbox.bind("<Return>", self.search_customer)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, command=self.search_customer
        )
        self.search_btn.pack(side="left", padx=8, pady=10)

        # Content Frame
        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        # Backend access
        self.backend = self.master.system.cus_manager

        # List all customers
        self.list_all_cus()

    def list_all_cus(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        scroll_frame = customtkinter.CTkScrollableFrame(self.result_area, width=700, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = customtkinter.CTkFrame(scroll_frame, fg_color=["#1f538d", "#3a6ea5"])
        header_frame.pack(fill="x", pady=(0, 5))
        customtkinter.CTkLabel(header_frame, text="ID", width=10, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="Name", width=30, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="Phone", width=20, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)

        customers = self.backend.list_cus()  # [(id, name, phone), ...]
        if not customers:
            customtkinter.CTkLabel(scroll_frame, text="No customers found.", font=("Arial", 18)).pack(pady=20)
            return

        # Display rows with hover & click
        for i, (cid, name, phone) in enumerate(customers):
            normal_color = ["#f0f0f0", "#e0e0e0"][i % 2]
            hover_color = "#a1c4fd"

            row_frame = customtkinter.CTkFrame(scroll_frame, fg_color=normal_color)
            row_frame.pack(fill="x", pady=2)

            def on_enter(e, frame=row_frame):
                frame.configure(fg_color=hover_color)

            def on_leave(e, frame=row_frame, color=normal_color):
                frame.configure(fg_color=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)

            # Click to edit
            row_frame.bind("<Button-1>", lambda e, cid=cid, name=name, phone=phone: self.edit_customer_popup(cid, name, phone))

            cus_id = customtkinter.CTkLabel(row_frame, text=str(cid), text_color="black", width=10, font=("Arial", 14))
            cus_id.pack(side="left", padx=10, pady=5, expand = True)
            cus_id.bind("<Enter>", on_enter)
            cus_id.bind("<Leave>", on_leave)
            cus_id.bind("<Button-1>", lambda e, cid=cid, name=name, phone=phone: self.edit_customer_popup(cid, name, phone))

            cus_name = customtkinter.CTkLabel(row_frame, text=name, text_color="black", width=30, font=("Arial", 14))
            cus_name.pack(side="left", padx=10, pady=5, expand = True)
            cus_name.bind("<Enter>", on_enter)
            cus_name.bind("<Leave>", on_leave)
            cus_name.bind("<Button-1>", lambda e, cid=cid, name=name, phone=phone: self.edit_customer_popup(cid, name, phone))

            cus_phone = customtkinter.CTkLabel(row_frame, text=phone, text_color="black", width=20, font=("Arial", 14))
            cus_phone.pack(side="left", padx=10, pady=5, expand = True)
            cus_phone.bind("<Enter>", on_enter)
            cus_phone.bind("<Leave>", on_leave)
            cus_phone.bind("<Button-1>", lambda e, cid=cid, name=name, phone=phone: self.edit_customer_popup(cid, name, phone))

    def edit_customer_popup(self, cid, name, phone):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Edit Customer")
        popup.geometry("400x300")

        name_var = customtkinter.StringVar(value=name)
        phone_var = customtkinter.StringVar(value=phone)

        customtkinter.CTkLabel(popup, text="Customer Name").pack(pady=10)
        name_entry = customtkinter.CTkEntry(popup, textvariable=name_var)
        name_entry.pack(pady=5)

        customtkinter.CTkLabel(popup, text="Phone Number").pack(pady=10)
        phone_entry = customtkinter.CTkEntry(popup, textvariable=phone_var)
        phone_entry.pack(pady=5)

        def submit():
            new_name = name_var.get().strip()
            new_phone = phone_var.get().strip()
            if new_name and new_phone:
                self.backend.remove(cid)  # remove old
                self.backend.add(new_name, new_phone)  # add new
                popup.destroy()
                self.list_all_cus()

        def delete():
            self.backend.remove(cid)
            popup.destroy()
            self.list_all_cus()

        customtkinter.CTkButton(popup, text="Save", command=submit).pack(pady=10)
        customtkinter.CTkButton(popup, text="Delete", fg_color="#ff4d4d", hover_color="#ff1a1a", command=delete).pack(pady=10)

    # Existing search/create functions remain unchanged
    def search_customer(self, event=None):
        keyword = self.searchbox.get().strip()

        # If search box is empty, show all customers
        if not keyword:
            self.list_all_cus()
            return

        # Otherwise, do normal search
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        result = self.backend.find_cus(keyword)
        if result is None:
            customtkinter.CTkLabel(self.result_area, text="Customer not found.", font=("Arial", 18, "bold")).pack(pady=10)
            customtkinter.CTkButton(self.result_area, text="Create New Profile", command=self.create_profile_popup).pack(pady=10)
            customtkinter.CTkButton(self.result_area, text="Cancel", command=self.clear_result).pack(pady=10)
            return

        cid, name, phone = result
        customtkinter.CTkLabel(self.result_area, text=f"Customer Found\n\nID: {cid}\nName: {name}\nPhone: {phone}", font=("Arial", 22, "bold")).pack(pady=20)

    def create_profile_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Create Customer")
        popup.geometry("400x300")
        name_var = customtkinter.StringVar()
        phone_var = customtkinter.StringVar()
        customtkinter.CTkLabel(popup, text="Customer Name").pack(pady=10)
        name_entry = customtkinter.CTkEntry(popup, textvariable=name_var)
        name_entry.pack(pady=5)
        customtkinter.CTkLabel(popup, text="Phone Number").pack(pady=10)
        phone_entry = customtkinter.CTkEntry(popup, textvariable=phone_var)
        phone_entry.pack(pady=5)
        popup.attributes('-topmost', True)
        def submit():
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            if name and phone:
                self.backend.add(name, phone)
                popup.destroy()
                self.list_all_cus()
        customtkinter.CTkButton(popup, text="Create", command=submit).pack(pady=20)

    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

class Dishes(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.label = customtkinter.CTkLabel(
            self.lbf, text="Dish Management", text_color="#D8D8D8",
            font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)


        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')
        self.searchvar = customtkinter.StringVar()
        self.icon = customtkinter.CTkLabel(self.searchf, text="🔍", font=("Segoe UI Emoji", 24))
        self.icon.pack(side="left", padx=8, pady=10)
        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar, placeholder_text='Search for dishes',
            fg_color=['gray90', 'gray16'], border_width=1, width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)
        # self.searchbox.bind("<Return>", self.search_dish)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, 
        )
        self.search_btn.pack(side="left", padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.dish_manager



    #NEEDED FILLING



    #Clear
    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


class Ingredients(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.label = customtkinter.CTkLabel(
            self.lbf, text="Ingredient Management", text_color="#D8D8D8",
            font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)


        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')
        self.searchvar = customtkinter.StringVar()
        self.icon = customtkinter.CTkLabel(self.searchf, text="🔍", font=("Segoe UI Emoji", 24))
        self.icon.pack(side="left", padx=8, pady=10)
        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar, placeholder_text='Search for ingredients',
            fg_color=['gray90', 'gray16'], border_width=1, width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)
        # self.searchbox.bind("<Return>", self.search_ingr)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120,
        )
        self.search_btn.pack(side="left", padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.ingr_manager



    #NEEDED FILLING



    #Clear
    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

class Orders(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.label = customtkinter.CTkLabel(
            self.lbf, text="Order Management", text_color="#D8D8D8",
            font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)


        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')
        self.searchvar = customtkinter.StringVar()
        self.icon = customtkinter.CTkLabel(self.searchf, text="🔍", font=("Segoe UI Emoji", 24))
        self.icon.pack(side="left", padx=8, pady=10)
        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar, placeholder_text='Search for orders',
            fg_color=['gray90', 'gray16'], border_width=1, width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)
        # self.searchbox.bind("<Return>", self.search_order)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, 
        )
        self.search_btn.pack(side="left", padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.order_manager



    #NEEDED FILLING



    #Clear
    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

class Employees(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.label = customtkinter.CTkLabel(
            self.lbf, text="Employees Management", text_color="#D8D8D8",
            font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)


        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')
        self.searchvar = customtkinter.StringVar()
        self.icon = customtkinter.CTkLabel(self.searchf, text="🔍", font=("Segoe UI Emoji", 24))
        self.icon.pack(side="left", padx=8, pady=10)
        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar, placeholder_text='Search for employees',
            fg_color=['gray90', 'gray16'], border_width=1, width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)
        # self.searchbox.bind("<Return>", self.search_emp)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, 
        )
        self.search_btn.pack(side="left", padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.emp_manager



    #NEEDED FILLING



    #Clear
    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)



class Root(customtkinter.CTk):
    def __init__(self, selected_frame):
        super().__init__()

        self.title("Food Delivery Management")
        self.geometry("1280x720")
        # self.attributes("-fullscreen", "True")
        # self.state("normal")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Fixed: Removed unnecessary connect() call - already handled in exe_query
        self.system=backend.System()
        # print(self.system.emp_manager.list_emp())

        self.SelectionBar = Selection_Frame(master=self)        
        self.SelectionBar.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="nsew")

        self.Dashboard = Dashboard(master=self)
        self.Dashboard.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.Customers = Customers(master=self)
        self.Customers.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.Dishes = Dishes(master=self)
        self.Dishes.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.Ingredients = Ingredients(master=self)
        self.Ingredients.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.Orders = Orders(master=self)
        self.Orders.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.Employees = Employees(master=self)
        self.Employees.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        show_frame(self, selected_frame)


   

#Mainloop
if __name__ == "__main__":
    root = Root(Dishes)
    root.update()

    root.mainloop()