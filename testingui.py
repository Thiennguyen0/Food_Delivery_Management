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
        # print(button.cget("font"))
        if button.cget("text") == sframe.__name__ or not button.cget("fg_color") == '#1f538d' or not button.cget("font") == ('Arial', 24, 'bold'):
            eval(f"root.SelectionBar.{sframe.__name__}.configure(fg_color='#1f538d', font=('Arial', 24, 'bold'))")
        else:
            eval(f"root.SelectionBar.{button.cget("text")}.configure(fg_color=['gray90', 'gray15'], font=('Arial', 24))")

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
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, weight=1)


        self.lbf = customtkinter.CTkFrame(self, corner_radius=10)
        self.lbf.grid(row=0,column=0,padx= 20, pady=20, sticky="nsew")
        self.label = customtkinter.CTkLabel(self.lbf, text="Dashboard Overview", text_color="#D8D8D8", font=('Segoe UI', 45, 'bold'))
        self.label.pack(padx=20,pady=20)



        self.contentf = customtkinter.CTkFrame(self)
        self.contentf.grid(row=1, column=0,padx=20, pady=(0,20),sticky="nsew")
        self.contentf.columnconfigure(1, weight=1)
        self.contentf.columnconfigure(2, weight=1)
        self.contentf.columnconfigure(3, weight=1)
        self.contentf.columnconfigure(0, weight=1)

        #Revenue
        self.revenuef = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.revenuef.grid(row=1,column=0,padx=20,pady=15, sticky="nsew")
        self.revenuef.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))
        self.revenuef.bind("<Leave>", lambda event2: on_leave(event2, self.revenuef,self.colors['leave']))

        self.revenuet = customtkinter.CTkLabel(self.revenuef, text=f"💰Total Revenue", text_color=self.colors['revenue1'], font=self.contentfont)

        self.revenue = customtkinter.CTkLabel(self.revenuef, text="revenue..", text_color=self.colors['revenue1'], font=self.numberfont)
        self.revenuet.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))
        self.revenue.bind("<Enter>", lambda event1: on_enter(event1, self.revenuef,self.colors['revenue2']))

        # self.revenuef.rowconfigure(0, weight=1)
        # self.revenuef.rowconfigure(1, weight=1)

        self.revenuet.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        self.revenue.grid(row=1,column=0,padx=25,pady=(0,25),stick="nsew")

        #Order
        self.orderf = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.orderf.grid(row=1,column=1,padx=20,pady=15, sticky="nsew")
        self.orderf.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.orderf.bind("<Leave>", lambda event2: on_leave(event2, self.orderf, self.colors['leave']))

        self.ordert = customtkinter.CTkLabel(self.orderf, text=f"🛒Orders ", text_color=self.colors['order1'], font=self.contentfont)

        self.order = customtkinter.CTkLabel(self.orderf, text="order..", text_color=self.colors['order1'], font=self.numberfont)
        self.ordert.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.order.bind("<Enter>", lambda event1: on_enter(event1, self.orderf, self.colors['order2']))
        self.ordert.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        self.order.grid(row=1,column=0,padx=25,pady=(0,25),stick="nsew")

        # Customers
        self.customersf = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.customersf.grid(row=1,column=2,padx=20,pady=15, sticky="nsew")
        self.customersf.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customersf.bind("<Leave>", lambda event2: on_leave(event2, self.customersf, self.colors['leave']))

        self.customerst = customtkinter.CTkLabel(self.customersf, text=f"👥Customers ", text_color=self.colors['info'], font=self.contentfont)

        self.customers = customtkinter.CTkLabel(self.customersf, text=f"{len(master.system.cus_manager.list_cus())}", text_color=self.colors['info'], font=self.numberfont)
        self.customerst.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customers.bind("<Enter>", lambda event1: on_enter(event1, self.customersf, self.colors['info']))
        self.customerst.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        self.customers.grid(row=1,column=0,padx=25,pady=(0,25),stick="nsew")

        #Menu Items
        self.menuitems = customtkinter.CTkFrame(self.contentf, border_width=3)
        self.menuitems.grid(row=1,column=3,padx=20,pady=15, sticky="nsew")
        self.menuitems.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menuitems.bind("<Leave>", lambda event2: on_leave(event2, self.menuitems, self.colors['leave']))

        self.menut = customtkinter.CTkLabel(self.menuitems, text=f"🍕Menu Items ", text_color=self.colors['order2'], font=self.contentfont)

        self.menu = customtkinter.CTkLabel(self.menuitems, text=f"{len(master.system.dish_manager.list_dishes())}", text_color=self.colors['order2'], font=self.numberfont)
        self.menut.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menu.bind("<Enter>", lambda event1: on_enter(event1, self.menuitems, self.colors['order1']))
        self.menut.grid(row=0,column=0,padx=25, pady=25,sticky="nsew")
        self.menu.grid(row=1,column=0,padx=25,pady=(0,25),stick="nsew")
        
class Customers(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Label = customtkinter.CTkLabel(self, text="Customers")
        self.Label.pack()

class Dishes(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.Label = customtkinter.CTkLabel(self, text="Dishes")
        self.Label.pack()

class Ingredients(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.Label = customtkinter.CTkLabel(self, text="Ingredients")
        self.Label.pack()

class Orders(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Label = customtkinter.CTkLabel(self, text="Orders")
        self.Label.pack()

class Employees(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Label = customtkinter.CTkLabel(self, text="Employees")
        self.Label.pack()



class Root(customtkinter.CTk):
    def __init__(self, selected_frame):
        super().__init__()

        self.title("Food Delivery Management")
        self.geometry("1280x720")
        # self.attributes("-fullscreen", "True")
        # self.state("normal")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        backend.connect()
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
root = Root(Dashboard)
root.mainloop()