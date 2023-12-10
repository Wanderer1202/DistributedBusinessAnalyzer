import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
import customtkinter as ctk
import random
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("C:/Users/user/Downloads/DistributedBusinessAnalyzer-main/Inputting App/blue.json")
appWidth, appHeight = 1000,800


class ProductEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Entry Application")
        self.root.geometry(f"{appWidth}*{appHeight}")

        self.product_id_label =ctk.CTkLabel(root, text="Product ID")
        self.product_id_label.grid(row=0, column=0,padx=20,pady=20,sticky="ew")
        self.product_id_entry =ctk.CTkEntry(root, state="readonly")
        self.product_id_entry.grid(row=0, column=1,padx=20,pady=20)
        self.generate_id_button =ctk.CTkButton(root, text="Generate ID", command=self.generate_product_id)
        self.generate_id_button.grid(row=0, column=2,padx=20,pady=20,sticky="ew")

        self.product_name_label = ctk.CTkLabel(root, text="Product Name")
        self.product_name_label.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
        self.product_name_entry = ctk.CTkEntry(root)
        self.product_name_entry.grid(row=1, column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.product_category_label = ctk.CTkLabel(root, text="Product Category")
        self.product_category_label.grid(row=2, column=0,padx=20,pady=20,sticky="ew")
        self.product_category_combo =ctk.CTkOptionMenu(root, values=["Food","Cosmetic","Electronic","Clothing","Pet_Food","Medicine","Stationary"])
        self.product_category_combo.grid(row=2,column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.unit_price_label = ctk.CTkLabel(root, text="Unit Price")
        self.unit_price_label.grid(row=3, column=0)
        self.unit_price_entry = ctk.CTkEntry(root)
        self.unit_price_entry.grid(row=3, column=1,columnspan=2,padx=20,pady=20,sticky="ew")
        
        self.cost_price_label = ctk.CTkLabel(root, text="Cost Price")
        self.cost_price_label.grid(row=4, column=0)
        self.cost_price_entry = ctk.CTkEntry(root)
        self.cost_price_entry.grid(row=4, column=1,padx=20,columnspan=2,pady=20,sticky="ew")

        self.manufacturing_country_label = ctk.CTkLabel(root, text="Manufacturing Country:")
        self.manufacturing_country_label.grid(row=5, column=0)
        self.manufacturing_country_combo =ctk.CTkOptionMenu(root, values=["USA", "China","Koean", "Japan", "India", "Germany","Myanmar","Thailand"])
        self.manufacturing_country_combo.grid(row=5, column=1,columnspan=2,padx=20,pady=20,sticky="ew")

        self.submit_button = ctk.CTkButton(root, text="Submit", command=self.save_to_database)
        self.submit_button.grid(row=6, column=2,padx=20,pady=20,sticky="ew")

        

        # Database connection setup
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="phyomaw",
            password="PMK@2023",
            database="supermarket"
        )
        self.cursor = self.db_connection.cursor()

        # ...

    def generate_product_id(self):
        new_id = random.randint(1000, 9999)
        while new_id in self.get_existing_ids():
            new_id = random.randint(1000, 9999)
        self.product_id_entry.configure(state="normal")
        self.product_id_entry.delete(0, "end")
        self.product_id_entry.insert(0, str(new_id))
        self.product_id_entry.configure(state="readonly")

    def get_existing_ids(self):
        try:
            self.cursor.execute("SELECT ProductID FROM product_dim")
            existing_ids = [row[0] for row in self.cursor.fetchall()]
            return existing_ids
        except mysql.connector.Error:
            return []

    def save_to_database(self):
        product_id = self.product_id_entry.get()
        product_name = self.product_name_entry.get()
        product_category = self.product_category_combo.get()
        unit_price = self.unit_price_entry.get()
        cost_price = self.cost_price_entry.get()
        manufacturing_country = self.manufacturing_country_combo.get()

        if not product_id or not product_name or not product_category or not unit_price or not manufacturing_country or not cost_price:
            messagebox.showerror("Error", "All fields are required!")
            return
        if float(cost_price)>=float(unit_price):
            messagebox.showerror("Error", "The value of unit pice must be larger than cost price!")
            return

        try:
            # Check if the product name already exists
            self.cursor.execute("SELECT ProductName FROM product_dim WHERE ProductName=%s", (product_name,))
            existing_product = self.cursor.fetchone()

            if existing_product:
                messagebox.showerror("Error", f"The product '{product_name}' already exists!")
                return

            insert_query = "INSERT INTO product_dim (ProductID, ProductName, ProductCategory, UnitPrice, ManufacturingCountry, CostPrice) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (product_id, product_name, product_category, unit_price, manufacturing_country, cost_price)
            self.cursor.execute(insert_query, values)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Product information saved to the database!")

        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "An error occurred while saving product information to the database.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ProductEntryApp(root)
    root.mainloop()
