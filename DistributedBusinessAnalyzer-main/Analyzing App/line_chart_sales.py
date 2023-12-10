import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import customtkinter as ctk
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("D:/UIT Projects/DistributedBusinessAnalyzer/Inputting App/blue.json")
appWidth, appHeight = 1000,800
def showgraph():
    x_column = "Date"  # X axis will always be Date
    y_column = ycombovalue.get()
    color_option = colorvalue.get()
    
    if y_column:
        filtered_df = apply_filters(merged_df2)
        sorted_data = sorted(zip(filtered_df[x_column], filtered_df[y_column]))

        sorted_dates, sorted_values = zip(*sorted_data)
        plt.plot(sorted_dates, sorted_values, marker='o', color=color_option)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"{y_column} over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def connect_database():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="phyomaw",
        password="PMK@2023",
        database="supermarket")
    return db_connection

def update_dataframe():
    products_df = pd.read_sql_query(product_query, db_connection)
    branches_df = pd.read_sql_query(branches_query, db_connection)
    sales_df = pd.read_sql_query(sales_query, db_connection)
    merged_df = pd.merge(branches_df, sales_df, on="BranchID")
    merged_df2 = pd.merge(merged_df, products_df, on="ProductID")
    return merged_df2

def apply_filters(data_frame):
    
    filter_category = category_combobox.get()
    filter_product = product_combobox.get()

    filtered_df = data_frame.copy()

    
    if filter_category!="All":
        filtered_df = filtered_df[filtered_df["ProductCategory"] == filter_category]
    if filter_product!="All":
        filtered_df = filtered_df[filtered_df["ProductName"] == filter_product]

    return filtered_df

def refresh_data():
    global db_connection
    db_connection.close()
    db_connection = connect_database()
    global merged_df2
    merged_df2 = update_dataframe()
    messagebox.showinfo("Success", "All data is refreshed")

# Connect to your database
db_connection = connect_database()

product_query = "SELECT * FROM product_dim"
branches_query = "SELECT * FROM branches_dim"
sales_query = "SELECT * FROM sales_fact"

merged_df2 = update_dataframe()

top =ctk.CTk()
top.title("Line Chart")
top.geometry(f"{appWidth}*{appHeight}")
ycombolabel = ctk.CTkLabel(top, text="Choose Y axis")
ycombolabel.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
ycombovalue = ctk.CTkOptionMenu(top, values=["SoldQuantity", "SalesAmount", "UnitPrice","Investment", "Profit"])
ycombovalue.grid(row=1, column=1,padx=20,pady=20,sticky="ew")

colorlabel = ctk.CTkLabel(top, text="Choose color")
colorlabel.grid(row=2, column=0,padx=20,pady=20,sticky="ew")
colorvalue = ctk.CTkOptionMenu(top, values=["red", "blue", "yellow", "green"])
colorvalue.grid(row=2, column=1,padx=20,pady=20,sticky="ew")

category_label = ctk.CTkLabel(top, text="Filter by Category:")
category_label.grid(row=3, column=0,padx=20,pady=20,sticky="ew")
product_categories = list(merged_df2["ProductCategory"].unique())
product_categories.insert(0, "All")  # Adding "All" at the beginning of the list
category_combobox = ctk.CTkOptionMenu(top, values=product_categories)
category_combobox.grid(row=3,column=1,padx=20,pady=20,sticky="ew")

product_label = ctk.CTkLabel(top, text="Filter by Product:")
product_label.grid(row=4, column=0,padx=20,pady=20,sticky="ew")
product_names = list(merged_df2["ProductName"].unique())
product_names.insert(0, "All")  # Adding "All" at the beginning of the list
product_combobox = ctk.CTkOptionMenu(top, values=product_names)
product_combobox.grid(row=4,column=1,padx=20,pady=20,sticky="ew")



showgraphbutton =  ctk.CTkButton(top, text="Show Line Chart", command=showgraph)
showgraphbutton.grid(row=5, column=0,padx=20,pady=20,sticky="ew")
refreshbutton =  ctk.CTkButton(top, text="Refresh Data", command=refresh_data)
refreshbutton.grid(row=5, column=1,padx=20,pady=20,sticky="ew")

top.mainloop()
