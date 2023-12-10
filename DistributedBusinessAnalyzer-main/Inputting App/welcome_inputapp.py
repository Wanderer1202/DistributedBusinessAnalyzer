import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("C:/Users/user/Downloads/DistributedBusinessAnalyzer-main/Inputting App/blue.json")
appWidth, appHeight = 1000,800



class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry(f"{appWidth}*{appHeight}")


        self.add_product_button = ctk.CTkButton(root, text="Add Product",command=self.open_product_input)
        self.add_product_button.grid(row=1,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.add_sales_button = ctk.CTkButton(root, text="Add Inventory", command=self.open_inventory_input)
        self.add_sales_button.grid(row=2,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.add_sales_button = ctk.CTkButton(root, text="Add Sales", command=self.open_sales_input)
        self.add_sales_button.grid(row=3,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.add_branch_button = ctk.CTkButton(root, text="Add Branch", command=self.open_branch_input)
        self.add_branch_button.grid(row=4,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

       
    def open_product_input(self):
        try:
            subprocess.run(["python", "product_input.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening product input: {e}")

    def open_branch_input(self):
        try:
            subprocess.run(["python", "branches_input.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening branch input: {e}")

    def open_sales_input(self):
        try:
            subprocess.run(["python", "sales_input.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening sales input: {e}")
    def open_inventory_input(self):
        try:
            subprocess.run(["python", "inventory_input.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening sales input: {e}")
            

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()

