import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime,date
from tkcalendar import DateEntry 
import customtkinter as ctk
import subprocess
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("D:/UIT Projects/DistributedBusinessAnalyzer/Inputting App/blue.json")
appWidth, appHeight = 1000,800

def showgraph():
    x_column = xcombovalue.get()
    
    color_option = colorvalue.get()

    
    if x_column :
        filtered_df = apply_filters(arrivals_sold)
        filtered_df["In-Stock"]=filtered_df["NewArrivals"]-filtered_df["SoldQuantity"]
        plt.bar(filtered_df[x_column], filtered_df["In-Stock"], color=color_option)
        plt.xlabel(x_column)
        plt.ylabel("In-Stock")
        plt.title(f"In Stock Inventory by {x_column}")
        plt.show()

def connect_database():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="phyomaw",
        password="PMK@2023",
        database="supermarket")
    return db_connection


def update_dataframe():
    inventory_df=pd.read_sql_query(inventory_query,db_connection)
    sales_df2 = pd.read_sql_query(sales_query2, db_connection)
    products_df = pd.read_sql_query(product_query, db_connection)
    branches_df = pd.read_sql_query(branches_query, db_connection)
    total_arrivals=inventory_df.groupby(["ProductID","BranchID"]).sum()
    total_sold = sales_df2.groupby(["ProductID", "BranchID"]).sum()
    total_arrivals.reset_index(inplace=True)
    total_sold.reset_index(inplace=True)

        
    arrivals_sold = pd.merge(total_arrivals, total_sold, on=["ProductID", "BranchID"])

    #filtered_df2=filtered_df2.fillna(0)
    arrivals_sold=pd.merge(arrivals_sold,branches_df,on=["BranchID"])
    #arrivals_sold=pd.merge(arrivals_sold,branches_df,on=["BranchID"])
    arrivals_sold=pd.merge(arrivals_sold,products_df,on=["ProductID"])
    return arrivals_sold
def apply_filters(data_frame):
    
    filter_category = category_combobox.get()
    filter_product = product_combobox.get()

    filtered_df = data_frame.copy()

    
    if (filter_category!="All"):
        filtered_df = filtered_df[filtered_df["ProductCategory"] == filter_category]
    if (filter_product!="All"):
        filtered_df = filtered_df[filtered_df["ProductName"] == filter_product]

    return filtered_df

def refresh_data():
    top.destroy()  # Destroy the current window
    try:
        subprocess.run(["python", "bar_chart_inventory.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Error opening sales input: {e}")

db_connection = connect_database()
product_query = "SELECT * FROM product_dim"
branches_query = "SELECT * FROM branches_dim"
sales_query = "SELECT * FROM sales_fact"
sales_query2="SELECT ProductID,BranchID,SoldQuantity FROM sales_fact"
inventory_query="select ProductID,BranchID,NewArrivals from inventory_fact"
#merged_df2 = update_dataframe()

inventory_df=pd.read_sql_query(inventory_query,db_connection)
sales_df2 = pd.read_sql_query(sales_query2, db_connection)
products_df = pd.read_sql_query(product_query, db_connection)
branches_df = pd.read_sql_query(branches_query, db_connection)
arrivals_sold=update_dataframe()

top = ctk.CTk()
top.title("Inventory")
top.geometry(f"{appWidth}*{appHeight}")
xcombolabel = ctk.CTkLabel(top, text="Choose X axis")
xcombolabel.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
xcombovalue = ctk.CTkOptionMenu(top, values=["BranchName", "Region", "City"])
xcombovalue.grid(row=1, column=1,padx=20,pady=20,sticky="ew")

colorlabel = ctk.CTkLabel(top, text="Choose color")
colorlabel.grid(row=3, column=0)
colorvalue =  ctk.CTkOptionMenu(top, values=["red", "blue", "yellow", "green"])
colorvalue.grid(row=3, column=1,padx=20,pady=20,sticky="ew")

# Filtering options


category_label = ctk.CTkLabel(top, text="Filter by Category")
category_label.grid(row=6, column=0,padx=20,pady=20,sticky="ew")
product_categories = list(arrivals_sold["ProductCategory"].unique())
product_categories.insert(0, "All")  # Adding "All" at the beginning of the list
category_combobox = ctk.CTkOptionMenu(top, values=product_categories)
category_combobox.grid(row=6,column=1,padx=20,pady=20,sticky="ew")

product_label = ctk.CTkLabel(top, text="Filter by Product")
product_label.grid(row=7, column=0,padx=20,pady=20,sticky="ew")
product_names = list(arrivals_sold["ProductName"].unique())
product_names.insert(0, "All")  # Adding "All" at the beginning of the list
product_combobox = ctk.CTkOptionMenu(top, values=product_names)
product_combobox.grid(row=7,column=1,padx=20,pady=20,sticky="ew")

showgraphbutton =  ctk.CTkButton(top, text="Show Graph", command=showgraph)
showgraphbutton.grid(row=8, column=0,padx=20,pady=20,sticky="ew")
refreshbutton =  ctk.CTkButton(top, text="Refresh", command=refresh_data)
refreshbutton.grid(row=8, column=1,padx=20,pady=20,sticky="ew")

top.mainloop()


