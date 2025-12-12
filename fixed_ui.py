import customtkinter
import backend
import datetime
import json

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
            getattr(root.SelectionBar, sframe.__name__).configure(fg_color='#1f538d', font=('Arial', 24, 'bold'))
        elif button.cget("text") != sframe.__name__:
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
        self.customers.grid(row=1,column=0,padx=25,pady=(0,25),sticky="nsew")

        #Menu items
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

        self.addbtn = customtkinter.CTkButton(self.searchf, text = "ADD NEW", width=120, command=self.create_profile_popup)
        self.addbtn.pack(side='right', padx=8, pady=10)

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

        customers = self.backend.list_cus()
        if not customers:
            customtkinter.CTkLabel(scroll_frame, text="No customers found.", font=("Arial", 18)).pack(pady=20)
            return

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
                self.backend.update(new_name, new_phone, cid)
                self.after(50, lambda: (
                    popup.destroy(),
                    self.list_all_cus()
                ))

        def delete():
            self.backend.remove(cid)
            popup.destroy()
            self.list_all_cus()

        popup.after(10, popup.lift)
        popup.after(20, popup.focus_force)

        customtkinter.CTkButton(popup, text="Save", command=submit).pack(pady=10)
        customtkinter.CTkButton(popup, text="Delete", fg_color="#ff4d4d", hover_color="#ff1a1a", command=delete).pack(pady=10)

    def search_customer(self, event=None):
        keyword = self.searchbox.get().strip()

        if not keyword:
            self.list_all_cus()
            return

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
        phone_entry.bind("<Return>", lambda x: submit())

        popup.attributes('-topmost', True)
        def submit():
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            if name and phone:
                self.backend.add(name, phone)
                popup.destroy()
                self.list_all_cus()

        popup.after(10, popup.lift)
        popup.after(20, popup.focus_force)

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
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, 
        )
        self.search_btn.pack(side="left", padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.dish_manager

        #list_all
        self.list_all_dishes()
    
    #list_all_dishes_method
    def list_all_dishes(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        scroll_frame = customtkinter.CTkScrollableFrame(self.result_area, width=700, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = customtkinter.CTkFrame(scroll_frame, fg_color=["#1f538d", "#3a6ea5"])
        header_frame.pack(fill="x", pady=(0, 5))
        customtkinter.CTkLabel(header_frame, text="Dish ID", width=10, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="Dish name", width=30, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="Cooking time", width=10, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="Dish price", width=20, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)

        dishes = self.backend.list_dishes()
        if not dishes:
            customtkinter.CTkLabel(scroll_frame, text="No dish found.", font=("Arial", 18)).pack(pady=20)
            return

        # Display rows with hover & click
        for i, (dish_id, dish_name, cooking_time, dish_price) in enumerate(dishes):
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
            row_frame.bind("<Button-1>", lambda e, dish_id = dish_id,
                            dish_name=dish_name, cooking_time = cooking_time,
                              dish_price = dish_price: self.edit_customer_popup(dish_id, dish_name, cooking_time, dish_price))

            d_id = customtkinter.CTkLabel(row_frame, text=str(dish_id), text_color="black", width=10, font=("Arial", 14))
            d_id.pack(side="left", padx=10, pady=5, expand = True)
            d_id.bind("<Enter>", on_enter)
            d_id.bind("<Leave>", on_leave)
            d_id.bind("<Button-1>", lambda e, dish_id = dish_id,
                            dish_name=dish_name, cooking_time = cooking_time,
                              dish_price = dish_price: self.edit_customer_popup(dish_id, dish_name, cooking_time, dish_price))

            d_name = customtkinter.CTkLabel(row_frame, text=dish_name, text_color="black", width=30, font=("Arial", 14))
            d_name.pack(side="left", padx=10, pady=5, expand = True)
            d_name.bind("<Enter>", on_enter)
            d_name.bind("<Leave>", on_leave)
            d_name.bind("<Button-1>", lambda e, dish_id = dish_id,
                            dish_name=dish_name, cooking_time = cooking_time,
                              dish_price = dish_price: self.edit_customer_popup(dish_id, dish_name, cooking_time, dish_price))
            
            time = customtkinter.CTkLabel(row_frame, text=cooking_time, text_color="black", width=20, font=("Arial", 14))
            time.pack(side="left", padx=10, pady=5, expand = True)
            time.bind("<Enter>", on_enter)
            time.bind("<Leave>", on_leave)
            time.bind("<Button-1>", lambda e, dish_id = dish_id,
                            dish_name=dish_name, cooking_time = cooking_time,
                              dish_price = dish_price: self.edit_customer_popup(dish_id, dish_name, cooking_time, dish_price))
            
            d_price = customtkinter.CTkLabel(row_frame, text=dish_price, text_color="black", width=20, font=("Arial", 14))
            d_price.pack(side="left", padx=10, pady=5, expand = True)
            d_price.bind("<Enter>", on_enter)
            d_price.bind("<Leave>", on_leave)
            d_price.bind("<Button-1>", lambda e, dish_id = dish_id,
                            dish_name=dish_name, cooking_time = cooking_time,
                              dish_price = dish_price: self.edit_customer_popup(dish_id, dish_name, cooking_time, dish_price))
            
    def edit_customer_popup(self, dish_id, dish_name, cooking_time, dish_price):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Edit Dish")
        popup.geometry("400x300")

        name_var = customtkinter.StringVar(value=dish_name)
        time_var = customtkinter.StringVar(value=cooking_time)
        price_var = customtkinter.IntVar(value=dish_price)


        customtkinter.CTkLabel(popup, text="Dish name").pack(pady=10)
        name_entry = customtkinter.CTkEntry(popup, textvariable=name_var)
        name_entry.pack(pady=5)

        customtkinter.CTkLabel(popup, text="Cooking time").pack(pady=10)
        time_entry = customtkinter.CTkEntry(popup, textvariable=time_var)
        time_entry.pack(pady=5)

        customtkinter.CTkLabel(popup, text="Dish price").pack(pady=10)
        price_entry = customtkinter.CTkEntry(popup, textvariable=price_var)
        price_entry.pack(pady=5)

        def submit():
            new_name = name_var.get().strip()
            new_time = time_entry.get().strip()
            new_price = price_entry.get()
            if new_name and new_time and new_price:
                self.backend.update_dish(new_name, new_time, new_price, dish_id)
                popup.destroy()
                self.list_all_dishes()

        def delete():
            pass
            self.backend.remove(dish_id)
            popup.destroy()
            self.list_all_dishes()

        customtkinter.CTkButton(popup, text="Save", command=submit).pack(pady=10)
        customtkinter.CTkButton(popup, text="Delete", fg_color="#ff4d4d", hover_color="#ff1a1a", command=delete).pack(pady=10)
        customtkinter.CTkButton(popup, text="Edit ingredients", fg_color="green", hover_color="dark green").pack(padx = 10)
    
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
        self.searchbox.bind("<Return>", self.search_ingredient)
        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120, command=self.search_ingredient
        )
        self.search_btn.pack(side="left", padx=8, pady=10)

        self.addbtn = customtkinter.CTkButton(self.searchf, text = "ADD NEW", width=120, command=self.create_profile_popup)
        self.addbtn.pack(side='right', padx=8, pady=10)


        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)


        self.backend = self.master.system.ingr_manager


        self.list_all_ingr()

    def list_all_ingr(self):
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
        customtkinter.CTkLabel(header_frame, text="STOCK", width=10, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="UNIT", width=10, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="EXPIRY", width=20, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)
        customtkinter.CTkLabel(header_frame, text="SUPPLIERS", width=30, font=("Arial", 16, "bold")).pack(side="left", padx=10, pady=5, expand=True)


        Ingredients = self.backend.get_all()  # [(id, name, stock, unit, expire date, suppliers), ...]
        if not Ingredients:
            customtkinter.CTkLabel(scroll_frame, text="No ingredient found.", font=("Arial", 18)).pack(pady=20)
            return

        # Display rows with hover & click
        for i, (i_id, name, stock, unit, expiry, supply) in enumerate(Ingredients):
            normal_color = ["#f0f0f0", "#e0e0e0"][i % 2]
            hover_color = "#a1c4fd"

            row_frame = customtkinter.CTkFrame(scroll_frame, fg_color=normal_color)

            row_frame.columnconfigure(0, weight=1)
            row_frame.columnconfigure(1, weight=1)
            row_frame.columnconfigure(2, weight=1)
            row_frame.columnconfigure(3, weight=1)
            row_frame.columnconfigure(4, weight=1)
            row_frame.columnconfigure(5, weight=1)

            row_frame.pack(fill="x", pady=2)

            def on_enter(e, frame=row_frame):
                frame.configure(fg_color=hover_color)

            def on_leave(e, frame=row_frame, color=normal_color):
                frame.configure(fg_color=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)

            # Click to edit
            row_frame.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_id = customtkinter.CTkLabel(row_frame, text=str(i_id), width=10, text_color="black", font=("Arial", 14))
            ingr_id.pack(side="left", padx=10, pady=5, expand = True)
            ingr_id.bind("<Enter>", on_enter)
            ingr_id.bind("<Leave>", on_leave)
            ingr_id.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_name = customtkinter.CTkLabel(row_frame, text=name, width=30,text_color="black", font=("Arial", 14))
            ingr_name.pack(side="left", padx=10, pady=5, expand = True)
            ingr_name.bind("<Enter>", on_enter)
            ingr_name.bind("<Leave>", on_leave)
            ingr_name.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_stock = customtkinter.CTkLabel(row_frame, text=stock, width=10, text_color="black", font=("Arial", 14))
            ingr_stock.pack(side="left", padx=10, pady=5, expand = True)
            ingr_stock.bind("<Enter>", on_enter)
            ingr_stock.bind("<Leave>", on_leave)
            ingr_stock.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_unit = customtkinter.CTkLabel(row_frame, text=unit, width=10, text_color="black", font=("Arial", 14))
            ingr_unit.pack(side="left", padx=10, pady=5, expand = True)
            ingr_unit.bind("<Enter>", on_enter)
            ingr_unit.bind("<Leave>", on_leave)
            ingr_unit.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_expiry = customtkinter.CTkLabel(row_frame, text=expiry, width=20, text_color="black", font=("Arial", 14))
            ingr_expiry.pack(side="left", padx=10, pady=5, expand = True)
            ingr_expiry.bind("<Enter>", on_enter)
            ingr_expiry.bind("<Leave>", on_leave)
            ingr_expiry.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

            ingr_supply = customtkinter.CTkLabel(row_frame, text=supply, width=30, text_color="black", font=("Arial", 14))
            ingr_supply.pack(side="left", padx=10, pady=5, expand = True)
            ingr_supply.bind("<Enter>", on_enter)
            ingr_supply.bind("<Leave>", on_leave)
            ingr_supply.bind("<Button-1>", lambda e, i_id = i_id, name = name, stock = stock, unit = unit, expiry = expiry, supply = supply: self.edit_ingredient_popup(i_id, name, stock, unit, expiry, supply))

    def edit_ingredient_popup(self, i_id, name, stock, unit, expiry, supply):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Edit Ingredient")
        popup.geometry("400x500")

        name_var = customtkinter.StringVar(value=name)
        stock_var = customtkinter.StringVar(value=stock)
        unit_var = customtkinter.StringVar(value=unit)
        expiry_var = customtkinter.StringVar(value=expiry)
        supply_var = customtkinter.StringVar(value=supply)

        customtkinter.CTkLabel(popup, text="Ingridient Name").pack(pady=10)
        # name_entry = customtkinter.CTkEntry(popup, textvariable=name_var)
        # name_entry.pack(pady=5)

        customtkinter.CTkLabel(popup, text="Stock Number").pack(pady=10)
        stock_entry = customtkinter.CTkEntry(popup, textvariable=stock_var)
        stock_entry.bind("<Return>", lambda x: submit())
        stock_entry.pack(pady=5)

        # customtkinter.CTkLabel(popup, text="Unit").pack(pady=10)
        # stock_entry = customtkinter.CTkEntry(popup, textvariable=unit_var)
        # stock_entry.pack(pady=5)

        # customtkinter.CTkLabel(popup, text="Expiry").pack(pady=10)
        # stock_entry = customtkinter.CTkEntry(popup, textvariable=expiry_var)
        # stock_entry.pack(pady=5)

        # customtkinter.CTkLabel(popup, text="Supplier").pack(pady=10)
        # stock_entry = customtkinter.CTkEntry(popup, textvariable=supply_var)
        # stock_entry.pack(pady=5)

        def submit():
            new_stock = stock_var.get().strip()
            if new_stock:
                self.backend.update_stock(i_id, int(stock_var.get()))
                popup.destroy()
                self.list_all_ingr()

        def out_of_stock():
            self.backend.update_stock(i_id, 0)
            popup.destroy()
            self.list_all_ingr()

        popup.after(10, popup.lift)
        popup.after(20, popup.focus_force)

        customtkinter.CTkButton(popup, text="Save", command=submit).pack(pady=10)
        customtkinter.CTkButton(popup, text="Out of stock", fg_color="#ff4d4d", hover_color="#ff1a1a", command=out_of_stock).pack(pady=10)

    # Existing search/create functions remain unchanged
    def search_ingredient(self, event=None):
        keyword = self.searchbox.get().strip()

        # If search box is empty, show all customers
        if not keyword:
            self.list_all_ingr()
            return

        # Otherwise, do normal search
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        result = self.backend.find_ingr(keyword)
        if result is None:
            customtkinter.CTkLabel(self.result_area, text="Ingredient not found.", font=("Arial", 18, "bold")).pack(pady=10)
            customtkinter.CTkButton(self.result_area, text="Create New Profile", command=self.create_profile_popup).pack(pady=10)
            customtkinter.CTkButton(self.result_area, text="Cancel", command=self.clear_result).pack(pady=10)
            return
        result=dict(result)
        customtkinter.CTkLabel(self.result_area, text=f"{result}", font=("Arial", 22, "bold")).pack(pady=20)

    def create_profile_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Create Ingredient")
        popup.geometry("400x600")
        name_var = customtkinter.StringVar()
        stock_var = customtkinter.StringVar()
        unit_var = customtkinter.StringVar()
        expiry_var = customtkinter.StringVar()
        supplier_var = customtkinter.StringVar()
        customtkinter.CTkLabel(popup, text="Ingredient Name").pack(pady=10)
        name_entry = customtkinter.CTkEntry(popup, textvariable=name_var)
        name_entry.pack(pady=5)
        customtkinter.CTkLabel(popup, text="Stock Number").pack(pady=10)
        stock_entry = customtkinter.CTkEntry(popup, textvariable=stock_var)
        stock_entry.pack(pady=5)
        customtkinter.CTkLabel(popup, text="Unit").pack(pady=10)
        unit_entry = customtkinter.CTkEntry(popup, textvariable=unit_var)
        unit_entry.pack(pady=5)
        customtkinter.CTkLabel(popup, text="Expiry ('yyyy-mm-dd')").pack(pady=10)
        expiry_entry = customtkinter.CTkEntry(popup, textvariable=expiry_var)
        expiry_entry.pack(pady=5)
        customtkinter.CTkLabel(popup, text="Supplier").pack(pady=10)
        supplier_entry = customtkinter.CTkEntry(popup, textvariable=supplier_var)
        supplier_entry.pack(pady=5)
        supplier_entry.bind("<Return>", lambda x: submit())

        popup.attributes('-topmost', True)

        def submit():
            name = name_var.get().strip()
            stock = stock_var.get().strip()
            unit = unit_var.get().strip()
            expiry = expiry_var.get().strip()
            supplier = supplier_var.get().strip()
            if name and stock:
                self.backend.add(name, stock, unit, expiry, supplier)
                popup.destroy()
                self.list_all_ingr()

        popup.after(10, popup.lift)
        popup.after(20, popup.focus_force)

        customtkinter.CTkButton(popup, text="Create", command=submit).pack(pady=20)

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
            font=('Segoe UI', 40, 'bold')
        )
        self.label.pack(padx=20, pady=16)

        # Search + actions
        topf = customtkinter.CTkFrame(self)
        topf.grid(row=1, column=0, padx=20, pady=(12, 6), sticky='ew')
        topf.columnconfigure(0, weight=1)

        self.searchvar = customtkinter.StringVar()
        self.searchbox = customtkinter.CTkEntry(
            topf, textvariable=self.searchvar, placeholder_text='Search orders by id / name / phone',
            width=420, height=36
        )
        self.searchbox.grid(row=0, column=0, sticky='w', padx=(6,8))
        self.searchbox.bind("<Return>", lambda e: self.search_order())

        self.search_btn = customtkinter.CTkButton(topf, text="Search", width=100, command=self.search_order)
        self.search_btn.grid(row=0, column=1, padx=6)

        self.create_btn = customtkinter.CTkButton(topf, text="Create Order", width=140, command=self.open_create_order_popup)
        self.create_btn.grid(row=0, column=2, padx=6)

        # Content area (orders)
        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(6, 20), sticky='nsew')
        self.contentf.columnconfigure(0, weight=1)
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=12, pady=12)

        # backend references
        self.system = self.master.system
        self.order_m = self.system.order_manager
        self.cus_m = self.system.cus_manager
        self.dish_m = self.system.dish_manager
        self.ship_m = self.system.shipper_manager
        self.emp_m = self.system.emp_manager

        # store reference to any open inline panel (so we can close it)
        self.open_inline_panel = None

        # initial load
        self.load_all_orders()

    def clear_result(self):
        self.result_area.destroy()
        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=12, pady=12)
        self.open_inline_panel = None

    def load_all_orders(self):
        self.clear_result()
        rows = self.order_m.get_all_orders_details() or []
        if len(rows) == 0:
            customtkinter.CTkLabel(self.result_area, text="No orders found.", font=("Segoe UI", 16)).pack(pady=20)
            return

        scroll = customtkinter.CTkScrollableFrame(self.result_area, width=980)
        scroll.pack(fill="both", expand=True)

        for r in rows:
            self.create_order_card(scroll, r)

    def search_order(self):
        keyword = (self.searchvar.get() or "").strip().lower()
        if not keyword:
            self.load_all_orders()
            return

        rows = self.order_m.get_all_orders_details() or []
        matched = []
        for r in rows:
            order_id = r["order_id"]
            cus_name = (r["cus_name"] or "").lower()
            cus_phone = (r["cus_phone"] or "").lower()
            if keyword in str(order_id).lower() or keyword in cus_name or keyword in cus_phone:
                matched.append(r)

        self.clear_result()
        if not matched:
            customtkinter.CTkLabel(self.result_area, text="No matching orders.", font=("Segoe UI", 16)).pack(pady=20)
            return

        scroll = customtkinter.CTkScrollableFrame(self.result_area, width=980)
        scroll.pack(fill="both", expand=True)
        for r in matched:
            self.create_order_card(scroll, r)

    def create_order_card(self, parent, row):
        order_id = row["order_id"]
        dish_req = row["dish_req"]
        total_price = row["total_price"]
        order_time = row["order_time"]
        status = row["status"]
        cus_name = row["cus_name"]
        cus_phone = row["cus_phone"]

        card = customtkinter.CTkFrame(parent, fg_color=["#222222", "#1A1A1A"], corner_radius=10)
        card.pack(fill="x", pady=8, padx=8)

        # left infos
        infof = customtkinter.CTkFrame(card, fg_color="transparent")
        infof.grid(row=0, column=0, sticky="w", padx=12, pady=8)
        title = customtkinter.CTkLabel(infof, text=f"Order #{order_id}", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")
        meta = customtkinter.CTkLabel(infof, text=f"{cus_name} | {cus_phone} • {order_time}", font=("Segoe UI", 12))
        meta.grid(row=1, column=0, sticky="w", pady=(4,0))
        stat_lbl = customtkinter.CTkLabel(infof, text=f"Status: {status}", font=("Segoe UI", 13))
        stat_lbl.grid(row=2, column=0, sticky="w", pady=(6,0))
        price_lbl = customtkinter.CTkLabel(infof, text=f"Total: {total_price}", font=("Segoe UI", 13))
        price_lbl.grid(row=3, column=0, sticky="w", pady=(4,6))

        # right actions
        btnf = customtkinter.CTkFrame(card, fg_color="transparent")
        btnf.grid(row=0, column=1, sticky="e", padx=12, pady=8)
        customtkinter.CTkButton(btnf, text="View Details", width=120,
                                command=lambda oid=order_id, dr=dish_req: self.show_order_details(oid, dr)).pack(pady=6)
        customtkinter.CTkButton(btnf, text="Toggle Status", width=120,
                                command=lambda oid=order_id: self.update_status_cycle(oid)).pack(pady=6)
        customtkinter.CTkButton(btnf, text="Assign Delivery", width=120,
                                command=lambda c=card, oid=order_id: self.toggle_assign_delivery_panel(c, oid)).pack(pady=6)
        customtkinter.CTkButton(btnf, text="Create Bill", width=120,
                                command=lambda c=card, oid=order_id, total=total_price: self.toggle_create_bill_panel(c, oid, total)).pack(pady=6)

        # quick inline delivery summary if exists
        delivery = self.order_m.get_delivery_info(order_id)
        if delivery:
            addr, dist, fee, shipper_info = delivery["delivery_addr"], delivery["distance"], delivery["fee"], delivery["shipper_info"]
            qlbl = customtkinter.CTkLabel(infof, text=f"Delivery: {shipper_info} • {dist} km • {fee} VND", font=("Segoe UI", 11))
            qlbl.grid(row=4, column=0, sticky="w", pady=(6,6))
        else:
            qlbl = customtkinter.CTkLabel(infof, text=f"No delivery assigned", font=("Segoe UI", 11))
            qlbl.grid(row=4, column=0, sticky="w", pady=(6,6))

    def show_order_details(self, order_id, dish_req_raw):
        win = customtkinter.CTkToplevel(self)
        win.title(f"Order #{order_id} Details")
        win.geometry("680x520")

        customtkinter.CTkLabel(win, text=f"Order #{order_id}", font=("Segoe UI", 20, "bold")).pack(pady=10)

        dishes = []
        try:
            if isinstance(dish_req_raw, str):
                dishes = json.loads(dish_req_raw)
            else:
                dishes = dish_req_raw or []
        except Exception:
            dishes = []

        listf = customtkinter.CTkScrollableFrame(win, width=640, height=320)
        listf.pack(padx=12, pady=8, fill="both", expand=True)

        if not dishes:
            customtkinter.CTkLabel(listf, text="No dishes recorded.", font=("Segoe UI", 13)).pack(pady=12)
        else:
            for d in dishes:
                name = d.get("dish_name", f"Dish {d.get('dish_id','')}")
                qty = d.get("quantity", 1)
                price = d.get("price", 0)
                extras = []
                if d.get("toppings"):
                    extras.append("Toppings: " + ", ".join(d["toppings"]))
                if d.get("note"):
                    extras.append("Note: " + d["note"])

                frame = customtkinter.CTkFrame(listf, fg_color="transparent")
                frame.pack(fill="x", padx=6, pady=6)
                customtkinter.CTkLabel(frame, text=f"{name}", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
                customtkinter.CTkLabel(frame, text=f"Qty: {qty} — Price: {price}", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w")
                if extras:
                    customtkinter.CTkLabel(frame, text=" • ".join(extras), font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")

        try:
            rows = self.order_m.get_all_orders_details() or []
            found = None
            for r in rows:
                if r["order_id"] == order_id:
                    found = r
                    break
            if found:
                customtkinter.CTkLabel(win, text=f"Total: {found['total_price']}", font=("Segoe UI", 14)).pack(pady=6)
                customtkinter.CTkLabel(win, text=f"Time: {found['order_time']}", font=("Segoe UI", 11)).pack()
                customtkinter.CTkLabel(win, text=f"Status: {found['status']}", font=("Segoe UI", 11)).pack(pady=(0,8))
        except Exception:
            pass

        customtkinter.CTkButton(win, text="Close", command=win.destroy).pack(pady=10)

    def update_status_cycle(self, order_id):
        statuses = ["Chờ duyệt", "Đang giao", "Đã giao", "Đã hủy"]
        rows = self.order_m.get_all_orders_details() or []
        cur = None
        for r in rows:
            if r["order_id"] == order_id:
                cur = r["status"]
                break
        if cur not in statuses:
            next_status = statuses[0]
        else:
            next_status = statuses[(statuses.index(cur) + 1) % len(statuses)]
        self.order_m.update_status(order_id, next_status)
        self.load_all_orders()

    def open_create_order_popup(self):
        win = customtkinter.CTkToplevel(self)
        win.title("Create New Order")
        win.geometry("880x650")

        # fetch customers and dishes
        cus_list = self.cus_m.list_cus() or []
        dishes = self.dish_m.list_dishes() or []

        # top: customer
        topf = customtkinter.CTkFrame(win)
        topf.pack(fill="x", padx=12, pady=10)
        customtkinter.CTkLabel(topf, text="Customer:", font=("Segoe UI", 13)).pack(side="left", padx=(6,8))
        cus_map = {}
        cus_vals = []
        for c in cus_list:
            label = f"{c['cus_name']} | {c['cus_phone']} (id:{c['cus_id']})"
            cus_vals.append(label)
            cus_map[label] = c["cus_id"]
        cus_var = customtkinter.StringVar()
        cus_menu = customtkinter.CTkOptionMenu(topf, values=cus_vals, variable=cus_var, width=520)
        if cus_vals:
            cus_menu.set(cus_vals[0])
        cus_menu.pack(side="left", padx=6)

        # center: dish adding area
        centerf = customtkinter.CTkFrame(win)
        centerf.pack(fill="both", expand=True, padx=12, pady=6)

        left_list = customtkinter.CTkScrollableFrame(centerf, width=580)
        left_list.pack(side="left", fill="both", expand=True, padx=(0,8))
        right_summary = customtkinter.CTkFrame(centerf, width=260)
        right_summary.pack(side="right", fill="y", padx=(8,0))

        # dish options dict
        dish_map = {}
        dish_labels = []
        for d in dishes:
            label = f"{d['dish_name']} ({d['dish_price']}) (id:{d['dish_id']})"
            dish_map[label] = d
            dish_labels.append(label)

        selected_rows = []

        def add_dish_row(default_label=None):
            row = customtkinter.CTkFrame(left_list, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=6)

            dish_var = customtkinter.StringVar()
            opt = dish_labels if dish_labels else ["(no dishes found)"]
            menu = customtkinter.CTkOptionMenu(row, values=opt, variable=dish_var, width=320)
            menu.pack(side="left", padx=(6,6))
            if default_label and default_label in opt:
                menu.set(default_label)
            elif opt:
                menu.set(opt[0])

            qty_var = customtkinter.IntVar(value=1)
            qty_entry = customtkinter.CTkEntry(row, textvariable=qty_var, width=60)
            qty_entry.pack(side="left", padx=(6,6))

            note_var = customtkinter.StringVar()
            note_entry = customtkinter.CTkEntry(row, textvariable=note_var, placeholder_text="Note (optional)", width=240)
            note_entry.pack(side="left", padx=(6,6))

            def remove_row():
                try:
                    selected_rows.remove((row, dish_var, qty_var, note_var))
                except ValueError:
                    pass
                row.destroy()
                refresh_total()

            rm_btn = customtkinter.CTkButton(row, text="Remove", width=80, command=remove_row)
            rm_btn.pack(side="left", padx=(6,6))

            selected_rows.append((row, dish_var, qty_var, note_var))
            refresh_total()

        def refresh_total():
            total = 0
            for _r, dish_var, qty_var, _note in selected_rows:
                label = dish_var.get()
                if not label:
                    continue
                d = dish_map.get(label)
                if d:
                    price = d["dish_price"]
                    qty = max(1, int(qty_var.get() or 1))
                    total += price * qty
            total_var.set(total)

        total_var = customtkinter.IntVar(value=0)
        customtkinter.CTkLabel(right_summary, text="Order Summary", font=("Segoe UI", 14, "bold")).pack(pady=(12,8))
        total_display = customtkinter.CTkLabel(right_summary, textvariable=total_var, font=("Segoe UI", 16))
        total_display.pack(pady=(6,12))

        customtkinter.CTkButton(right_summary, text="Add Dish", width=160, command=add_dish_row).pack(pady=(6,6))

        def submit_order():
            # build dish_req_in list
            dish_req_in = []
            for _r, dish_var, qty_var, note_var in selected_rows:
                label = dish_var.get()
                if not label:
                    continue
                d = dish_map.get(label)
                if not d:
                    continue
                dish_obj = {
                    "dish_id": d["dish_id"],
                    "dish_name": d["dish_name"],
                    "quantity": max(1, int(qty_var.get() or 1)),
                    "price": d["dish_price"]
                }
                note = note_var.get().strip()
                if note:
                    dish_obj["note"] = note
                dish_req_in.append(dish_obj)

            if not dish_req_in:
                customtkinter.CTkLabel(win, text="Add at least one dish.", text_color="red").pack()
                return

            total_price = total_var.get()
            cus_key = cus_var.get()
            if not cus_key:
                customtkinter.CTkLabel(win, text="Select a customer.", text_color="red").pack()
                return
            cus_id = cus_map.get(cus_key)

            order_id = self.order_m.create_orders(dish_req_in, total_price, cus_id)
            if order_id:
                customtkinter.CTkLabel(win, text=f"Order created: #{order_id}", text_color="green").pack(pady=6)
                self.load_all_orders()
                win.destroy()
            else:
                customtkinter.CTkLabel(win, text="Failed to create order.", text_color="red").pack(pady=6)

        add_dish_row()
        def periodic_refresh():
            refresh_total()
            win.after(300, periodic_refresh)
        periodic_refresh()

        customtkinter.CTkButton(win, text="Create Order", width=200, command=submit_order).pack(pady=10)
        customtkinter.CTkButton(win, text="Cancel", width=140, command=win.destroy).pack()

    def toggle_assign_delivery_panel(self, card_widget, order_id):
        # close any currently open panel
        if self.open_inline_panel:
            try:
                self.open_inline_panel.destroy()
            except Exception:
                pass
            self.open_inline_panel = None
            if hasattr(card_widget, "_order_id") and getattr(card_widget, "_order_id") == order_id:
                return

        panel = customtkinter.CTkFrame(self.result_area, fg_color=["#2A2A2A", "#1D1D1D"], corner_radius=8)
        panel.pack(fill="x", padx=20, pady=(4,8))
        card_widget._order_id = order_id
        panel._order_id = order_id
        self.open_inline_panel = panel

        customtkinter.CTkLabel(panel, text=f"Assign Delivery for Order #{order_id}", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=8)

        # shippers list
        shippers = self.ship_m.get_all() or []
        ship_map = {}
        ship_vals = []
        for s in shippers:
            label = f"{s['shipper_info']} (id:{s['shipper_id']})"
            ship_vals.append(label)
            ship_map[label] = s["shipper_id"]
        ship_var = customtkinter.StringVar()
        ship_menu = customtkinter.CTkOptionMenu(panel, values=ship_vals, variable=ship_var, width=420)
        if ship_vals:
            ship_menu.set(ship_vals[0])
        ship_menu.grid(row=1, column=0, padx=12, pady=6, sticky="w")

        # address, distance, fee
        addr_var = customtkinter.StringVar()
        dist_var = customtkinter.DoubleVar(value=1.0)
        fee_var = customtkinter.DoubleVar(value=10000)

        customtkinter.CTkLabel(panel, text="Address:").grid(row=2, column=0, sticky="w", padx=12, pady=(6,2))
        customtkinter.CTkEntry(panel, textvariable=addr_var, width=560).grid(row=3, column=0, columnspan=2, padx=12, pady=(0,6))

        customtkinter.CTkLabel(panel, text="Distance (km):").grid(row=4, column=0, sticky="w", padx=12, pady=(6,2))
        customtkinter.CTkEntry(panel, textvariable=dist_var, width=120).grid(row=5, column=0, sticky="w", padx=12, pady=(0,6))

        customtkinter.CTkLabel(panel, text="Fee:").grid(row=4, column=1, sticky="w", padx=12, pady=(6,2))
        customtkinter.CTkEntry(panel, textvariable=fee_var, width=120).grid(row=5, column=1, sticky="w", padx=12, pady=(0,6))

        def submit_delivery():
            ship_key = ship_var.get()
            if not ship_key:
                customtkinter.CTkLabel(panel, text="Select shipper.", text_color="red").grid(row=7, column=0, padx=12, pady=6)
                return
            shipper_id = ship_map.get(ship_key)
            addr = addr_var.get().strip()
            dist = float(dist_var.get() or 0)
            fee = float(fee_var.get() or 0)
            res = self.order_m.add_delivery(order_id, shipper_id, addr, dist, fee)
            if res is not None:
                customtkinter.CTkLabel(panel, text="Delivery assigned.", text_color="green").grid(row=7, column=0, padx=12, pady=6)
                self.load_all_orders()
            else:
                customtkinter.CTkLabel(panel, text="Failed to assign delivery.", text_color="red").grid(row=7, column=0, padx=12, pady=6)

        submit_btn = customtkinter.CTkButton(panel, text="Assign Delivery", command=submit_delivery)
        submit_btn.grid(row=6, column=0, padx=12, pady=8, sticky="w")

        close_btn = customtkinter.CTkButton(panel, text="Close", command=lambda: (panel.destroy(), setattr(self, 'open_inline_panel', None)))
        close_btn.grid(row=6, column=1, padx=12, pady=8, sticky="e")

    def toggle_create_bill_panel(self, card_widget, order_id, total_amount):
        if self.open_inline_panel:
            try:
                self.open_inline_panel.destroy()
            except Exception:
                pass
            self.open_inline_panel = None
            if hasattr(card_widget, "_order_id") and getattr(card_widget, "_order_id") == order_id:
                return

        panel = customtkinter.CTkFrame(self.result_area, fg_color=["#2A2A2A", "#1D1D1D"], corner_radius=8)
        panel.pack(fill="x", padx=20, pady=(4,8))
        card_widget._order_id = order_id
        panel._order_id = order_id
        self.open_inline_panel = panel

        customtkinter.CTkLabel(panel, text=f"Create Bill for Order #{order_id}", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=8)

        emps = self.emp_m.list_emp() or []
        ships = self.ship_m.get_all() or []

        emp_map = {}
        emp_vals = []
        for e in emps:
            label = f"{e['emp_name']} (id:{e['emp_id']})"
            emp_vals.append(label)
            emp_map[label] = e["emp_id"]
        emp_var = customtkinter.StringVar()
        emp_menu = customtkinter.CTkOptionMenu(panel, values=emp_vals, variable=emp_var, width=420)
        if emp_vals:
            emp_menu.set(emp_vals[0])
        emp_menu.grid(row=1, column=0, padx=12, pady=6, sticky="w")

        ship_map = {}
        ship_vals = []
        for s in ships:
            label = f"{s['shipper_info']} (id:{s['shipper_id']})"
            ship_vals.append(label)
            ship_map[label] = s["shipper_id"]
        ship_var = customtkinter.StringVar()
        ship_menu = customtkinter.CTkOptionMenu(panel, values=ship_vals, variable=ship_var, width=420)
        if ship_vals:
            ship_menu.set(ship_vals[0])
        ship_menu.grid(row=1, column=1, padx=12, pady=6, sticky="w")

        customtkinter.CTkLabel(panel, text=f"Total amount: {total_amount}", font=("Segoe UI", 13)).grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=(8,6))

        def submit_bill():
            emp_key = emp_var.get()
            ship_key = ship_var.get()
            if not emp_key or not ship_key:
                customtkinter.CTkLabel(panel, text="Select employee and shipper.", text_color="red").grid(row=4, column=0, padx=12, pady=6)
                return
            emp_id = emp_map.get(emp_key)
            shipper_id = ship_map.get(ship_key)
            res = self.order_m.create_bill(order_id, emp_id, shipper_id, total_amount)
            if res is not None:
                customtkinter.CTkLabel(panel, text="Bill created.", text_color="green").grid(row=4, column=0, padx=12, pady=6)
                self.load_all_orders()
            else:
                customtkinter.CTkLabel(panel, text="Failed to create bill.", text_color="red").grid(row=4, column=0, padx=12, pady=6)

        customtkinter.CTkButton(panel, text="Create Bill", command=submit_bill).grid(row=3, column=0, padx=12, pady=8, sticky="w")
        customtkinter.CTkButton(panel, text="Close", command=lambda: (panel.destroy(), setattr(self, 'open_inline_panel', None))).grid(row=3, column=1, padx=12, pady=8, sticky="e")


class Employees(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.backend = self.master.system.emp_manager

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.lbf = customtkinter.CTkFrame(self, fg_color=['gray90', 'gray13'])
        self.lbf.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")

        self.label = customtkinter.CTkLabel(
            self.lbf, text="Employees Management",
            text_color="#D8D8D8", font=('Segoe UI', 50, 'bold')
        )
        self.label.pack(padx=20, pady=20)

        self.searchf = customtkinter.CTkFrame(self)
        self.searchf.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='nsew')

        self.searchvar = customtkinter.StringVar()

        customtkinter.CTkLabel(
            self.searchf, text="🔍", font=("Segoe UI Emoji", 24)
        ).pack(side="left", padx=8, pady=10)

        self.searchbox = customtkinter.CTkEntry(
            self.searchf, textvariable=self.searchvar,
            placeholder_text='Search for employees',
            fg_color=['gray90', 'gray16'], border_width=1,
            width=200, height=40
        )
        self.searchbox.pack(side="left", padx=(0, 8), pady=10)

        self.search_btn = customtkinter.CTkButton(
            self.searchf, text="Search", width=120,
            command=self.search_emp
        )
        self.search_btn.pack(side="left", padx=8, pady=10)

        customtkinter.CTkButton(
            self.searchf, text="Add New Employee",
            fg_color="green", hover_color="#0A8F00",
            command=self.add_emp_popup, width=150
        ).pack(side="right", padx=10)

        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=2, column=0, padx=20, pady=(15, 20), sticky='nsew')

        self.result_area = None
        self.list_all_emp()

    def list_all_emp(self, employees=None):
        if self.result_area:
            self.result_area.destroy()

        self.result_area = customtkinter.CTkFrame(self.contentf)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)

        scroll_frame = customtkinter.CTkScrollableFrame(self.result_area, width=700, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # HEADER
        header = customtkinter.CTkFrame(scroll_frame, fg_color=["#1f538d", "#3a6ea5"])
        header.pack(fill="x", pady=(0, 5))

        for text in ["ID", "Name", "Bill Count"]:
            customtkinter.CTkLabel(
                header, text=text, font=("Arial", 16, "bold"),
                width=80
            ).pack(side="left", padx=10, pady=5, expand=True)

        if employees is None:
            emp_data = self.backend.count_bill()
        else:
            emp_data = employees

        if not emp_data:
            customtkinter.CTkLabel(scroll_frame, text="No employee found.", font=("Arial", 18)).pack(pady=20)
            return

        for i, (eid, name, count) in enumerate(emp_data):
            normal_color = ["#f0f0f0", "#e0e0e0"][i % 2]
            hover_color = "#a1c4fd"

            row = customtkinter.CTkFrame(scroll_frame, fg_color=normal_color)
            row.pack(fill="x", pady=2)

            row.bind("<Enter>", lambda e, frame=row: frame.configure(fg_color=hover_color))
            row.bind("<Leave>", lambda e, frame=row, c=normal_color: frame.configure(fg_color=c))

            row.bind("<Button-1>", lambda e, eid=eid, name=name: self.edit_emp_popup(eid, name))

            for txt in [eid, name, count]:
                lbl = customtkinter.CTkLabel(row, text=str(txt), text_color="black", width=80, font=("Arial", 14))
                lbl.pack(side="left", padx=10, pady=5, expand=True)

                lbl.bind("<Enter>", lambda e, frame=row: frame.configure(fg_color=hover_color))
                lbl.bind("<Leave>", lambda e, frame=row, c=normal_color: frame.configure(fg_color=c))
                lbl.bind("<Button-1>", lambda e, eid=eid, name=name: self.edit_emp_popup(eid, name))

    def search_emp(self):
        key = self.searchvar.get().strip()

        if key == "":
            self.list_all_emp()
            return

        all_emp = self.backend.count_bill()
        result = [x for x in all_emp if key.lower() in x[1].lower()]

        self.list_all_emp(result)

    def add_emp_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Add Employee")
        popup.geometry("350x250")

        customtkinter.CTkLabel(popup, text="Employee Name", font=("Arial", 16)).pack(pady=15)

        name_var = customtkinter.StringVar()
        entry = customtkinter.CTkEntry(popup, textvariable=name_var, width=200)
        entry.pack(pady=10)

        def submit():
            name = name_var.get().strip()
            if name:
                self.backend.add(name)
                popup.destroy()
                self.list_all_emp()

        customtkinter.CTkButton(popup, text="Add", command=submit).pack(pady=15)

    def edit_emp_popup(self, eid, name):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Edit Employee")
        popup.geometry("350x300")

        customtkinter.CTkLabel(popup, text=f"Edit Employee #{eid}", font=("Arial", 18)).pack(pady=15)

        name_var = customtkinter.StringVar(value=name)
        entry = customtkinter.CTkEntry(popup, textvariable=name_var, width=200)
        entry.pack(pady=10)

        def update():
            new_name = name_var.get().strip()
            if new_name:
                self.backend.update(new_name, eid)
                popup.destroy()
                self.list_all_emp()

        def remove():
            self.backend.remove(eid)
            popup.destroy()
            self.list_all_emp()

        customtkinter.CTkButton(popup, text="Save", fg_color="blue", hover_color="#003C99",
                                command=update).pack(pady=10)

        customtkinter.CTkButton(popup, text="Remove", fg_color="red", hover_color="#AA0000",
                                command=remove).pack(pady=10)

class Root(customtkinter.CTk):
    def __init__(self, selected_frame):
        super().__init__()

        self.title("Food Delivery Management")
        self.geometry("1280x720")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.system=backend.System()

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
    root = Root(Dashboard)
    root.update()

    root.mainloop()