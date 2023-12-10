import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime,date
from tkcalendar import DateEntry 
import customtkinter as ctk
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("D:/UIT Projects/DistributedBusinessAnalyzer/Inputting App/blue.json")
appWidth, appHeight = 1000,800
def showgraph():
    x_column = xcombovalue.get()
    y_column = ycombovalue.get()
    color_option = colorvalue.get()
    
    if x_column and y_column:
        filtered_df = apply_filters(merged_df2)
        result=filtered_df[y_column].groupby(filtered_df[x_column]).sum()
        xaxis = result.index
        yaxis = result.values

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(xaxis, yaxis, color=color_option)

        # Add labels and title
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"{y_column} by {x_column}")

        # Rotate x-axis labels for better visibility (optional)
        plt.xticks(rotation=90)

        # Show the plot
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
    filter_date_from = date_from_entry.get()
    filter_date_to = date_to_entry.get()
    filter_category = category_combobox.get()
    filter_product = product_combobox.get()

    filtered_df = data_frame.copy()

    if filter_date_from and filter_date_to:
        frommonth, fromday, fromyear = map(int, filter_date_from.split('/'))
        formatted_from_date = f"20{fromyear:02d}-{frommonth:02d}-{fromday:02d}"
        tomonth, today, toyear = map(int, filter_date_to.split('/'))
        formatted_to_date = f"20{toyear:02d}-{tomonth:02d}-{today:02d}"
        filter_date_from = datetime.strptime(formatted_from_date, "%Y-%m-%d").date()  # Convert to datetime object
        filter_date_to = datetime.strptime(formatted_to_date, "%Y-%m-%d").date()  # Convert to datetime object
        filtered_df = filtered_df[(filtered_df["Date"] >= filter_date_from) & (filtered_df["Date"] <= filter_date_to)]
    if (filter_category!="All"):
        filtered_df = filtered_df[filtered_df["ProductCategory"] == filter_category]
    if (filter_product!="All"):
        filtered_df = filtered_df[filtered_df["ProductName"] == filter_product]

    return filtered_df

def refresh_data():
    global db_connection
    db_connection.close()
    db_connection = connect_database()
    global merged_df2
    merged_df2 = update_dataframe()
    messagebox.showinfo("Success", "All data is refreshed")

db_connection = connect_database()
product_query = "SELECT * FROM product_dim"
branches_query = "SELECT * FROM branches_dim"
sales_query = "SELECT * FROM sales_fact"
inventory_query="select * from inventory_fact"
merged_df2 = update_dataframe()

top = ctk.CTk()
top.title("Bar Chart")
top.geometry(f"{appWidth}*{appHeight}")
xcombolabel = ctk.CTkLabel(top, text="Choose X axis")
xcombolabel.grid(row=1, column=0,padx=20,pady=20,sticky="ew")
xcombovalue = ctk.CTkOptionMenu(top, values=["ProductCategory", "ProductName", "BranchName", "Region", "City", "ManufacturingCountry"])
xcombovalue.grid(row=1, column=1,padx=20,pady=20,sticky="ew")
ycombolabel = ctk.CTkLabel(top, text="Choose Y axis")
ycombolabel.grid(row=2, column=0,padx=20,pady=20,sticky="ew")
ycombovalue = ctk.CTkOptionMenu(top, values=["SoldQuantity", "SalesAmount", "UnitPrice", "Investment", "Profit"])
ycombovalue.grid(row=2, column=1,padx=20,pady=20,sticky="ew")
colorlabel = ctk.CTkLabel(top, text="Choose color")
colorlabel.grid(row=3, column=0,padx=20,pady=20,sticky="ew")
colorvalue = ctk.CTkOptionMenu(top, values=["red", "blue", "yellow", "green"])
colorvalue.grid(row=3, column=1,padx=20,pady=20,sticky="ew")

# Filtering options
date_from_label = ctk.CTkLabel(top, text="Filter from Date")
date_from_label.grid(row=5, column=0,padx=20,pady=20,sticky="ew")
date_from_entry = DateEntry(top)  # Use DateEntry from tkcalendar
date_from_entry.grid(row=5, column=1,padx=20,pady=20,sticky="ew")

date_to_label = ctk.CTkLabel(top, text="Filter to Date")
date_to_label.grid(row=5, column=2,padx=20,pady=20,sticky="ew")
date_to_entry = DateEntry(top)  # Use DateEntry from tkcalendar
date_to_entry.grid(row=5, column=3,padx=20,pady=20,sticky="ew")

category_label = ctk.CTkLabel(top, text="Filter by Category")
category_label.grid(row=6, column=0,padx=20,pady=20,sticky="ew")
product_categories = list(merged_df2["ProductCategory"].unique())
product_categories.insert(0, "All")  # Adding "All" at the beginning of the list
category_combobox = ctk.CTkOptionMenu(top, values=product_categories)
category_combobox.grid(row=6,column=1,padx=20,pady=20,sticky="ew")

product_label = ctk.CTkLabel(top, text="Filter by Product:")
product_label.grid(row=7, column=0,padx=20,pady=20,sticky="ew")
product_names = list(merged_df2["ProductName"].unique())
product_names.insert(0, "All")  # Adding "All" at the beginning of the list
product_combobox = ctk.CTkOptionMenu(top, values=product_names)
product_combobox.grid(row=7,column=1,padx=20,pady=20,sticky="ew")

showgraphbutton =ctk.CTkButton(top, text="Show Graph", command=showgraph)
showgraphbutton.grid(row=8, column=1,padx=20,pady=20,sticky="ew")
refreshbutton = ctk.CTkButton(top, text="Refresh", command=refresh_data)
refreshbutton.grid(row=8, column=2,padx=20,pady=20,sticky="ew")

top.mainloop()


