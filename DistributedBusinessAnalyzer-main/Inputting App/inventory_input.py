import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import customtkinter as ctk
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("C:/Users/user/Downloads/DistributedBusinessAnalyzer-main/Inputting App/blue.json")
appWidth, appHeight = 2000,800
class InventoryEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Entry Application")
        self.root.geometry(f"{appWidth}*{appHeight}")

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="phyomaw",
            password="PMK@2023",
            database="supermarket"
        )
        self.cursor = self.db_connection.cursor()

        self.product_names = self.load_product_names()  # Load product names
        self.branch_names = self.load_branch_names()
        self.date_label =  ctk.CTkLabel(root, text="Date:")
        self.date_label.grid(row=0, column=0,padx=20,pady=20,sticky="ew")
        self.date_calendar = Calendar(root, selectmode='day',
                                      year=datetime.now().year,
                                      month=datetime.now().month,
                                      day=datetime.now().day)
        self.date_calendar.grid(row=0, column=1,padx=20,pady=20,sticky="ew")

        self.product_id_label =  ctk.CTkLabel(root, text="Product Name")  # Updated label text
        self.product_id_label.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
        self.product_id_combo =  ctk.CTkOptionMenu(root, values=self.product_names)  # Use product_names
        self.product_id_combo.grid(row=1, column=1,padx=20,pady=20,sticky="ew")

        self.branch_id_label =  ctk.CTkLabel(root, text="Branch Name")  # Updated label text
        self.branch_id_label.grid(row=2, column=0,padx=20,pady=20,sticky="ew")
        self.branch_id_combo =  ctk.CTkOptionMenu(root, values=self.branch_names)  # Use branch_names
        self.branch_id_combo.grid(row=2, column=1,padx=20,pady=20,sticky="ew")

        self.newarrival_label =  ctk.CTkLabel(root, text="New Arrival")
        self.newarrival_label.grid(row=3, column=0,padx=20,pady=20,sticky="ew")
        self.newarrival_entry =  ctk.CTkEntry(root)
        self.newarrival_entry.grid(row=3, column=1,padx=20,pady=20,sticky="ew")

        self.submit_button = ctk.CTkButton(root, text="Submit", command=self.save_to_database)
        self.submit_button.grid(row=4, column=2,padx=20,pady=20,sticky="ew")
    def load_branch_names(self):
        try:
            self.cursor.execute("SELECT BranchName FROM branches_dim")
            branch_names = [row[0] for row in self.cursor.fetchall()]  # Load branch names
            return branch_names
        except mysql.connector.Error:
            return []

    def load_product_names(self):
        try:
            self.cursor.execute("SELECT ProductName FROM product_dim")
            product_names = [row[0] for row in self.cursor.fetchall()]  # Load product names
            return product_names
        except mysql.connector.Error:
            return []

    

    

    def save_to_database(self):
        selected_date = self.date_calendar.get_date()
        month, day, year = map(int, selected_date.split('/'))
        formatted_date = f"20{year:02d}-{month:02d}-{day:02d}"
    
        product_name = self.product_id_combo.get()  # Get selected product name
        branch_name = self.branch_id_combo.get()  # Get selected branch name
        new_arrival = self.newarrival_entry.get()
        if int(new_arrival)>=1000000:
            messagebox.showerror("Error", "Invalid input!. New Arrival must be less than 1000000")
            return

        if not selected_date or not product_name or not branch_name or not new_arrival:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            new_arrival = int(new_arrival)
        except ValueError:
            messagebox.showerror("Error", "New Arrival must be an integer!")
            return

        # Get ProductID from product_dim based on selected product name
        product_id = self.get_product_id_by_name(product_name)
        if product_id is None:
            messagebox.showerror("Error", "Invalid Product Name!")
            return

         # Get BranchID from branches_dim based on selected branch name
        branch_id = self.get_branch_id_by_name(branch_name)
        if branch_id is None:
            messagebox.showerror("Error", "Invalid Branch Name!")
            return

        try:
            insert_query = "INSERT INTO inventory_fact (Date, ProductID, BranchID, NewArrivals) VALUES (%s, %s, %s, %s)"
            values = (formatted_date, product_id, branch_id, new_arrival)
            self.cursor.execute(insert_query, values)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Inventory information saved to the database!")
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "An error occurred while saving inventory information to the database.")
        
    def get_product_id_by_name(self, product_name):
        try:
            self.cursor.execute("SELECT ProductID FROM product_dim WHERE ProductName = %s", (product_name,))
            product_id = self.cursor.fetchone()
            if product_id:
                return product_id[0]
            return None
        except mysql.connector.Error:
            return None

    def get_branch_id_by_name(self, branch_name):
        try:
            self.cursor.execute("SELECT BranchID FROM branches_dim WHERE BranchName = %s", (branch_name,))
            branch_id = self.cursor.fetchone()
            if branch_id:
                return branch_id[0]
            return None
        except mysql.connector.Error:
            return None


    
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = InventoryEntryApp(root)
    root.mainloop()
