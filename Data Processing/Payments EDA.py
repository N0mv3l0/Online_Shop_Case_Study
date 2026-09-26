# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC #PAYMENTS EDA

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Ingestion

# COMMAND ----------

payments=spark.read.table("online.shop.payments")

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib as plt

pmt= payments.toPandas()

display(pmt)

# COMMAND ----------

#Check the total rows and columns from the table
pmt.shape

# COMMAND ----------

#Summary of the table
# Notice the PaymentDate is stored as a text
pmt.info()

# COMMAND ----------

#sum of duplicates in the table

pmt.duplicated().sum()

# COMMAND ----------

#Counting the NULL values in each column
pmt.isnull().sum()

# COMMAND ----------

#Count of unique payment status options

pmt["PaymentStatus"].value_counts()