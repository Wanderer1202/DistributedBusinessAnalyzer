import tkinter as tk
from tkinter import messagebox
import subprocess
import customtkinter as ctk
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("D:/UIT Projects/DistributedBusinessAnalyzer/Inputting App/blue.json")
appWidth, appHeight = 1000,800


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry(f"{appWidth}*{appHeight}")

        self.add_product_button =ctk.CTkButton(root, text="Analyze Sales with Bar Chart", command=self.open_bar_chart_sales)
        self.add_product_button.grid(row=1,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.add_branch_button = ctk.CTkButton(root, text="Time Series Analysis of Sales", command=self.open_line_chart_sales)
        self.add_branch_button.grid(row=2,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.add_sales_button = ctk.CTkButton(root, text="Analyze In-Stock Values", command=self.open_bar_chart_inventory)
        self.add_sales_button.grid(row=3,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

    def open_bar_chart_sales(self):
        try:
            subprocess.run(["python", "bar_chart_sales.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening product input: {e}")

    def open_line_chart_sales(self):
        try:
            subprocess.run(["python", "line_chart_sales.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening branch input: {e}")

    def open_bar_chart_inventory(self):
        try:
            subprocess.run(["python", "bar_chart_inventory.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error opening sales input: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()

