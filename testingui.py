import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#global functions

def show_frame(root, sframe):
    for button in root.SelectionBar.winfo_children()[1:]:
        if button.cget("text") == sframe.__name__:
            eval(f"root.SelectionBar.{sframe.__name__}.configure(fg_color='#1f538d')")
        else:
            eval(f"root.SelectionBar.{button.cget("text")}.configure(fg_color=['gray90', 'gray15'])")

    for frame in root.winfo_children()[1:]:
        if not isinstance(frame, sframe):
            frame.grid_forget()
        else:
            frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")



#Class definition

class Selection_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Label = customtkinter.CTkLabel(self, text="Food Delivery\nManagement", font=("Arial", 55, "bold"), pady=25)
        self.Label.grid(row = 0, column = 0, padx = 20, pady=20, sticky="ew")

        self.Dashboard = customtkinter.CTkButton(self, text="Dashboard", font=("Arial", 24), command=self.Afunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Dashboard.grid(row = 1, column = 0, padx = 10, pady=20, sticky="ew")

        self.Customers = customtkinter.CTkButton(self, text="Customers", font=("Arial", 24), command=self.Bfunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Customers.grid(row = 2, column = 0, padx = 10, pady=20, sticky="ew")

        self.Dishes = customtkinter.CTkButton(self, text="Dishes", font=("Arial", 24), command=self.Cfunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Dishes.grid(row = 3, column = 0, padx = 10, pady=20, sticky="ew")

        self.Ingredients = customtkinter.CTkButton(self, text="Ingredients", font=("Arial", 24), command=self.Dfunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Ingredients.grid(row = 4, column = 0, padx = 10, pady=20, sticky="ew")

        self.Orders = customtkinter.CTkButton(self, text="Orders", font=("Arial", 24), command=self.Efunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Orders.grid(row = 5, column = 0, padx = 10, pady=20, sticky="ew")

        self.Employees = customtkinter.CTkButton(self, text="Employees", font=("Arial", 24), command=self.Ffunc, height=70, corner_radius=20, fg_color=["gray90", "gray15"], border_color=["gray90", "gray12"], border_width=2)
        self.Employees.grid(row = 6, column = 0, padx = 10, pady=20, sticky="ew")


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

        self.Label = customtkinter.CTkLabel(self, text="Dashboard")
        self.Label.pack()
        
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

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

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