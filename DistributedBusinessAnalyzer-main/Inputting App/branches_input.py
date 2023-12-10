import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import customtkinter as ctk
import random
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("C:/Users/user/Downloads/DistributedBusinessAnalyzer-main/Inputting App/blue.json")
appWidth, appHeight = 1000,800

class BranchInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Branch Input Application")

        

        # Connect to the database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="phyomaw",
            password="PMK@2023",  # Replace with your password
            database="supermarket"   # Replace with your database name
        )
        self.cursor = self.db_connection.cursor()

        # Branch ID
        self.branch_id_label = ctk.CTkLabel(root, text="Branch ID")
        self.branch_id_label.grid(row=0, column=0,padx=20,pady=20,sticky="ew")
        self.branch_id_entry = ctk.CTkEntry(root, state="readonly")
        self.branch_id_entry.grid(row=0, column=1,padx=20,pady=20,sticky="ew")
        self.generate_id_button = ctk.CTkButton(root, text="Generate ID", command=self.generate_branch_id)
        self.generate_id_button.grid(row=0, column=2,padx=20,pady=20,sticky="ew")

        # Branch Name
        self.branch_name_label = ctk.CTkLabel(root, text="Branch Name")
        self.branch_name_label.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
        self.branch_name_entry = ctk.CTkEntry(root)
        self.branch_name_entry.grid(row=1, column=1,padx=20,pady=20,sticky="ew")

        # City
        self.city_label = ctk.CTkLabel(root, text="City")
        self.city_label.grid(row=2, column=0)
        self.city_combo =ctk.CTkOptionMenu(root, values=["Yangon","Mandalay","Taunggyi"])
        self.city_combo.grid(row=2, column=1,padx=20,pady=20,sticky="ew")

        # Region
        self.region_label = ctk.CTkLabel(root, text="Region")
        self.region_label.grid(row=3, column=0)
        self.region_combo = ctk.CTkOptionMenu(root, values=["Yangon Region","Mandalay Region","Shan State"])
        self.region_combo.grid(row=3, column=1,padx=20,pady=20,sticky="ew")

        

        # Submit button
        self.submit_button =  ctk.CTkButton(root, text="Submit", command=self.save_to_database)
        self.submit_button.grid(row=4, column=2,padx=20,pady=20,sticky="ew")

    def generate_branch_id(self):
        new_id = random.randint(1000, 9999)
        while new_id in self.get_existing_ids():
            new_id = random.randint(1000, 9999)
        self.branch_id_entry.configure(state="normal")
        self.branch_id_entry.delete(0, "end")
        self.branch_id_entry.insert(0, str(new_id))
        self.branch_id_entry.configure(state="readonly")

    def get_existing_ids(self):
        try:
            self.cursor.execute("SELECT BranchID FROM branches_dim")
            existing_ids = [row[0] for row in self.cursor.fetchall()]
            return existing_ids
        except mysql.connector.Error:
            return []

    def save_to_database(self):
        branch_id = self.branch_id_entry.get()
        branch_name = self.branch_name_entry.get()
        city = self.city_combo.get()
        region = self.region_combo.get()

        if not branch_id or not branch_name or not city or not region:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            self.cursor.execute("INSERT INTO branches_dim (BranchID, BranchName, City, Region) VALUES (%s, %s, %s, %s)",
                                (branch_id, branch_name, city, region))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Branch information saved to the database!")
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "An error occurred while saving branch information to the database.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = BranchInputApp(root)
    root.mainloop()
