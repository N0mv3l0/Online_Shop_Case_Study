# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
products=spark.read.table("online.shop.products")

# COMMAND ----------

# MAGIC %md
# MAGIC #PRODUCTS EDA

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Ingestion

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib as plt

prd= products.toPandas()

display(prd)

# COMMAND ----------

#how many distinct products

prd["ProductName"].unique()





# COMMAND ----------

prd["ProductName"].value_counts()

# how many distinct products- counting total of each value

# COMMAND ----------

#Count of distinct Category
prd["Category"].value_counts()

# COMMAND ----------

#summary of the table
prd.info()

# COMMAND ----------

prd.duplicated().sum()

# COMMAND ----------

#statistical summary of the numeric column

prd["UnitPrice"].describe()