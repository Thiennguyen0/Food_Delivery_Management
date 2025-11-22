import customtkinter

# def hide_all_widgets(parent_widget):
#     for widget in parent_widget.winfo_children():
#         widget.pack_forget()



customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

class Selection_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.Label = customtkinter.CTkLabel(self, text="Sidebar", font=("Arial", 55, "bold"), pady=25)
        self.Label.pack(pady=30)


        self.buttonA = customtkinter.CTkButton(self, text="buttonA", font=("Arial", 24), height=50, width = 250)
        self.buttonA.pack(pady=30)

        self.buttonB = customtkinter.CTkButton(self, text="buttonB", font=("Arial", 24), height=50, width = 250)
        self.buttonB.pack(pady=30)

        self.buttonC = customtkinter.CTkButton(self, text="buttonC", font=("Arial", 24), height=50, width = 250)
        self.buttonC.pack(pady=30)

        self.buttonD = customtkinter.CTkButton(self, text="buttonD", font=("Arial", 24), height=50, width = 250)
        self.buttonD.pack(pady=30)

        self.buttonE = customtkinter.CTkButton(self, text="buttonE", font=("Arial", 24), height=50, width = 250)
        self.buttonE.pack(pady=30)

        self.buttonF = customtkinter.CTkButton(self, text="buttonF", font=("Arial", 24), height=50, width = 250)
        self.buttonF.pack(pady=30)
    
    def Afunc(self):
        pass

    def Bfunc(self):
        pass
    
    def Cfunc(self):
        pass
    
    def Dfunc(self):
        pass
    
    def Efunc(self):
        pass
    
    def Ffunc(self):
        pass


class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Food Delivery Management")
        self.geometry("1280x720")

        self.SelectionBar = Selection_Frame(master=self)
        self.SelectionBar.grid(row=0, column=0, padx=20, pady=20)

root = Root()
root.mainloop()