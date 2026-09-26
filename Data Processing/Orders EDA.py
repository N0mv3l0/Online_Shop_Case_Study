# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC #ORDERS EDA

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Ingestion

# COMMAND ----------

orders= spark.read.table("online.shop.orders")

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib as plt

od= orders.toPandas()

display(od)

# COMMAND ----------

#shows the number of rows and columns
od.shape

# COMMAND ----------

#extract the summary of stats from the numerical data
od.describe() 

# COMMAND ----------

#summary of each column in the table

od.info()

# COMMAND ----------

#sum of duplicates in the table

od.duplicated().sum()

# COMMAND ----------

od.duplicated()    #checks for duplicates in each row. FALSE= no duplicate. TRUE= duplicated row

# COMMAND ----------

#Counting the NULL values in each column
od.isnull().sum()

# COMMAND ----------

#Fixing the null values in the table
od["Discount"] = od["Discount"].fillna(0)


# COMMAND ----------

#Fixing the null values in the table
od["PaymentMethod"] = od["PaymentMethod"].fillna("Unknown")

# COMMAND ----------

# Investigating the null values on the Quantity Column
od[od["Quantity"].isnull()]


# COMMAND ----------

# Since the the status shows mostly "Completed" and not "Canceled", it does not make sense to replace NULLL values in the Quantity column with a zero.
# check the status distribution of the rows where the Quantity is NULL.
# Most orders are completed, then the NUll values under "Quantity" remains NULL

od[od["Quantity"].isnull()]["Status"].value_counts()

# COMMAND ----------

#Investigating order date
# Check details/rows where the date shows NULL

od[od["OrderDate"].isnull()]

# COMMAND ----------

#Further investigation where the OrderDate is NULL
# I have decided to leave the NULL orderDate as NULL since the status is COMPLETED, this means all transactions were succesfully completed. It makes no sense to drop those NULL values because the outcome will be affected.
od[od["OrderDate"].isnull()][["OrderID", "Status", "Quantity", "PaymentMethod"]]

# COMMAND ----------

#Final check of null values
od.isnull().sum()

# COMMAND ----------

od.count()          #counts the number of non null values in each column

# COMMAND ----------

# Where the booleon shows "True", it means there is duplicates. This code removes duplicated rows.
# Next step- check the shape of the table. Old= 50120   New= 50000 rows
od.drop_duplicates(inplace=True)

# COMMAND ----------

#Count of unique payment method types

od["PaymentMethod"].value_counts()

# COMMAND ----------

#Counts the total of unique status type in the column
od["Status"].value_counts()

# COMMAND ----------

#Step 1: Convert the column to datetime format (just in case it is currently stored as text)
od['OrderDate'] = pd.to_datetime(od['OrderDate'])

# Step 2: Extract the componentsod['year'] = od['OrderDate'].dt.year
od['month'] = od['OrderDate'].dt.month
od['day'] = od['OrderDate'].dt.day
od['day_name'] = od['OrderDate'].dt.day_name()

# COMMAND ----------

display(od)

# COMMAND ----------

od.shape

# COMMAND ----------

# MAGIC %md
# MAGIC I want to join the customers table to orders table on CustomerID.
# MAGIC I think the first step is to call the customers to this notebook.
# MAGIC Then inner join on CustomerID.

# COMMAND ----------

# MAGIC %md
# MAGIC # 1. Run the customer notebook to load the 'cts' dataframe into this session

# COMMAND ----------

# MAGIC %run.//Workspace/Users/nomvelogcaba@gmail.com/Online_shop/Online_Shop_Case_Study/Data Processing/Customers EDA

# COMMAND ----------

. Use pandas merge to join them directly
final_pandas_df = od.merge(cts, on="CustomerID", how="inner")