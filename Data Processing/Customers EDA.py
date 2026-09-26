# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC #Customers EDA

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Ingestion

# COMMAND ----------

customers= spark.read.table("online.shop.customers")


# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib as plt

cts= customers.toPandas()

display(cts)

# COMMAND ----------

#Check the total rows and columns from the table
cts.shape

# COMMAND ----------

#Summary of the table
# Notice age is stored as a float and SignupDate as a text
cts.info()

# COMMAND ----------

cts.describe

# COMMAND ----------

cts["City"].unique()
#Notice the different spelling of "Tehran" and "Mashad"- they need to be cleaned.

# COMMAND ----------

cts["City"] = cts["City"].replace({"tehran": "Tehran", "Mashhad": "Mashad" , "NULL":"None"})
#Cleaning the city names using the .replace function. "tehran" to "Tehran" and "Mashhad" to "Mashad"

# COMMAND ----------

cts["City"].unique()

# COMMAND ----------

#Checking for NULL values in Age column
#Notice, there are a lot of NULL values in Age column, so we cannot drop because data will be inconsistent. Age column to be cleaned.
cts[cts["Age"].isnull()]

# COMMAND ----------

#NULL Age will be replaced with the average age
cts["Age"] = cts["Age"].fillna(cts["Age"].mean())

# COMMAND ----------

cts["Age"].agg(["min", "median", "max"])
#Finding the min, max, and middle age because I want to create age buckets in the Case Statement

# COMMAND ----------

#Case statement for AGE
import pandas as pd
import numpy as np

# 1. Define the WHEN conditions
conditions = [
    (cts["Age"] >= 18) & (cts["Age"] <= 30),
    (cts["Age"] > 30) & (cts["Age"] <= 45),
    (cts["Age"] > 45) & (cts["Age"] <= 65)
]

# 2. Define the THEN results
choices = ["Young Adult", "Middle Aged", "Senior"]

# 3. Apply the conditions (The default acts like the ELSE statement)
cts["Age_Group"] = np.select(conditions, choices, default="Other")


# COMMAND ----------

cts["CustomerSegment"].unique()
#finding unique CustomerSegment types

# COMMAND ----------

#Check for the total of duplicates in the table
cts.duplicated().sum()

# COMMAND ----------

#Step 1: Convert the column to datetime format (just in case it is currently stored as text)
cts['SignupDate'] = pd.to_datetime(cts['SignupDate'])

# Step 2: Extract the componentsod['year'] = cts['OrderDate'].dt.year
cts['year'] = cts['SignupDate'].dt.year
cts['month'] = cts['SignupDate'].dt.month
cts['month_name'] = cts['SignupDate'].dt.month_name()
cts['day'] = cts['SignupDate'].dt.day
cts['day_name'] = cts['SignupDate'].dt.day_name()

# COMMAND ----------

display(cts)