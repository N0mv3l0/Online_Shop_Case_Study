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

# MAGIC %md
# MAGIC #Converting spark dataframe to pandas

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib as plt

od= orders.toPandas()

display(od)

# COMMAND ----------

# MAGIC %md
# MAGIC # EDA

# COMMAND ----------

#shows the number of rows and columns
od.shape

# COMMAND ----------

#extract the summary of stats from the numerical data
od.describe() 

# COMMAND ----------

#summary of each column in the table
# Notice that OrderDate is a text

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

od.count()          #counts the number of non null values in each column/ Counting the total number of rows per column.

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
od['year'] = od['OrderDate'].dt.year
od['month'] = od['OrderDate'].dt.month
od['day'] = od['OrderDate'].dt.day
od['day_name'] = od['OrderDate'].dt.day_name()

# COMMAND ----------

import numpy as np

# Checks the text names directly
od['day_type'] = np.where(od['day_name'].isin(['Saturday', 'Sunday']), 'Weekend', 'Weekday')


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
# MAGIC # Orders + Customers = cts_od

# COMMAND ----------

# MAGIC %md
# MAGIC # 1. Run the customer notebook to load the 'cts' dataframe into this session

# COMMAND ----------

# MAGIC %run "/Users/nomvelogcaba@gmail.com/Online_shop/Online_Shop_Case_Study/Data Processing/Customers EDA"
# MAGIC

# COMMAND ----------

# Now 'cts' is loaded from the other notebook, and you can merge it directly
cts_od = od.merge(cts, on="CustomerID", how="inner")


# COMMAND ----------

display(cts_od)

# COMMAND ----------

cts_od.shape

# COMMAND ----------

# MAGIC %md
# MAGIC #cts_od + products = cts_od_prd

# COMMAND ----------

# MAGIC %md
# MAGIC # Run the products notebook to load the 'prd' dataframe into this session

# COMMAND ----------

# MAGIC %run "/Users/nomvelogcaba@gmail.com/Online_shop/Online_Shop_Case_Study/Data Processing/Products EDA"

# COMMAND ----------

# Now 'prd' is loaded from the other notebook, and you can merge it directly
cts_od_prd = cts_od.merge(prd, on="ProductID", how="inner")

# COMMAND ----------

display(cts_od_prd)

# COMMAND ----------

cts_od_prd.shape

# COMMAND ----------

# MAGIC %md
# MAGIC # cts_od_prd + pmt = final_merged

# COMMAND ----------

# MAGIC %md
# MAGIC #Run the payments notebook to load the 'pmt' dataframe into this session

# COMMAND ----------

# MAGIC %run "/Users/nomvelogcaba@gmail.com/Online_shop/Online_Shop_Case_Study/Data Processing/Payments EDA"

# COMMAND ----------

# Now 'prd' is loaded from the other notebook, and you can merge it directly
final_merged = cts_od_prd.merge(pmt, on="OrderID", how="inner")

# COMMAND ----------

display(final_merged)

# COMMAND ----------

# MAGIC %md
# MAGIC # Final_merged EDA 

# COMMAND ----------

final_merged.shape

# COMMAND ----------

import numpy as np

# Calculate revenue for each order
final_merged['Revenue'] = final_merged['Quantity'] * final_merged['UnitPrice'] * (1 - final_merged['Discount'])


# COMMAND ----------

display(final_merged)

# COMMAND ----------

# MAGIC %md
# MAGIC #Final_merged EDA

# COMMAND ----------

import pandas as pd
import matplotlib.pyplot as plt

df= final_merged

# COMMAND ----------

#Check the table

df.head()

# COMMAND ----------

# Checking the rows ad columns of the combined table
df.shape 

# COMMAND ----------

print(df["Status"].value_counts())

# COMMAND ----------

print(df["PaymentStatus"].value_counts())

# COMMAND ----------

# MAGIC %md
# MAGIC # Revenue calculation
# MAGIC
# MAGIC We only recognise revenue when:
# MAGIC
# MAGIC Status = Completed
# MAGIC AND
# MAGIC PaymentStatus = Paid

# COMMAND ----------

analysis_df = df[
    (df["Status"] == "Completed") &
    (df["PaymentStatus"] == "Paid") &
    (df["Quantity"].notna()) &
    (df["OrderDate"].notna())
].copy()

# COMMAND ----------

#Peak and least month revenue calculation
import pandas as pd

# 1. Your existing filtered dataframe cleanup
analysis_df = df[
    (df["Status"] == "Completed") & 
    (df["PaymentStatus"] == "Paid") & 
    (df["Quantity"].notna()) & 
    (df["OrderDate"].notna())
].copy()

# 2. Ensure OrderDate is in datetime format
analysis_df["OrderDate"] = pd.to_datetime(analysis_df["OrderDate"])

# 3. Calculate Revenue per row (Adjust 'UnitPrice' if your column name is different)
# If you already have a 'TotalAmount' or 'Revenue' column, you can skip this step.
analysis_df["Revenue"] = analysis_df["Quantity"] * analysis_df["UnitPrice"]

# 4. Extract the Month-Year Period (e.g., '2026-01')
analysis_df["Month_Period"] = analysis_df["OrderDate"].dt.to_period("M")

# 5. Group by Month and sum the Revenue
monthly_revenue = analysis_df.groupby("Month_Period")["Revenue"].sum()

# 6. Find the peak and least months using idxmax() and idxmin()
peak_month = monthly_revenue.idxmax()
peak_revenue = monthly_revenue.max()

least_month = monthly_revenue.idxmin()
least_revenue = monthly_revenue.min()

# 7. Print the results
print(f"Peak Month: {peak_month} with Revenue of {peak_revenue:,.2f}")
print(f"Least Month: {least_month} with Revenue of {least_revenue:,.2f}")


# COMMAND ----------

import pandas as pd

# 1. Your filtered dataframe cleanup
analysis_df = df[
    (df["Status"] == "Completed") & 
    (df["PaymentStatus"] == "Paid") & 
    (df["Quantity"].notna()) & 
    (df["OrderDate"].notna())
].copy()

# 2. Ensure OrderDate is in datetime format
analysis_df["OrderDate"] = pd.to_datetime(analysis_df["OrderDate"])

# 3. Calculate Revenue per row (Change 'UnitPrice' if your column is named differently)
analysis_df["Revenue"] = analysis_df["Quantity"] * analysis_df["UnitPrice"]

# 4. Extract the Year
analysis_df["Year"] = analysis_df["OrderDate"].dt.year

# 5. Calculate Annual Revenue
# We convert the resulting Series to a DataFrame to make adding columns easy
annual_revenue = analysis_df.groupby("Year")["Revenue"].sum().to_frame()

# 6. Calculate the Year-over-Year (YoY) Percentage Difference
annual_revenue["YoY_Change_Percentage"] = annual_revenue["Revenue"].pct_change() * 100

# 7. Format for clean display
# Renames column for clarity and fills the first year's NaN value with 0 or a placeholder
annual_revenue["YoY_Change_Percentage"] = annual_revenue["YoY_Change_Percentage"].fillna(0)

print(annual_revenue)


# COMMAND ----------

print("Rows:", len(analysis_df))
print("Unique Orders:", analysis_df["OrderID"].nunique())

# COMMAND ----------

# MAGIC %md
# MAGIC #KPI Aggregation

# COMMAND ----------

total_revenue = analysis_df["Revenue"].sum()

total_orders = analysis_df["OrderID"].nunique()

total_units = analysis_df["Quantity"].sum()

aov = total_revenue / total_orders

print("Total Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Total Units:", total_units)
print("AOV:", round(aov, 2))

# COMMAND ----------

print(df.shape)
print(df["OrderID"].nunique())

print(analysis_df.shape)
print(analysis_df["OrderID"].nunique())

# COMMAND ----------

#Checking order distribution with dfferent payment status and orders_status
print(
    df.groupby(["Status", "PaymentStatus"])
      .size()
      .reset_index(name="Orders")
)

# COMMAND ----------

#Checking if OrderID is duplicated
print(
    df["OrderID"].duplicated().sum()
)

# COMMAND ----------

analysis_df["Year"] = analysis_df["OrderDate"].dt.year

analysis_df["Month"] = analysis_df["OrderDate"].dt.month

analysis_df["Month_Name"] = analysis_df["OrderDate"].dt.month_name()

analysis_df["Day_Name"] = analysis_df["OrderDate"].dt.day_name()

# COMMAND ----------

analysis_df["Year_Month"] = (
    analysis_df["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)

# COMMAND ----------

display(analysis_df)

# COMMAND ----------

#Monthly revenue check

monthly_revenue = (
    analysis_df
    .groupby("Year_Month")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("OrderID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

monthly_revenue.head()

# COMMAND ----------

# MAGIC %md
# MAGIC #Monthly revenue

# COMMAND ----------

#Line graph for Monthly_Revenue

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["Year_Month"],
    monthly_revenue["Revenue"],
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Category revenue

# COMMAND ----------

#Category revenue

category_analysis = (
    analysis_df
    .groupby("Category")
    .agg(
        Revenue=("Revenue", "sum"),
        Units=("Quantity", "sum"),
        Orders=("OrderID", "nunique")
    )
    .reset_index()
)

#sort

category_analysis = category_analysis.sort_values(
    "Revenue",
    ascending=False
)

print(category_analysis)

# COMMAND ----------

#Graph for Category Revenue

plt.figure(figsize=(10, 6))

plt.bar(
    category_analysis["Category"],
    category_analysis["Revenue"]
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Product Revenue

# COMMAND ----------

product_analysis = (
    analysis_df
    .groupby("ProductName")
    .agg(
        Revenue=("Revenue", "sum"),
        Units=("Quantity", "sum"),
        Orders=("OrderID", "nunique")
    )
    .reset_index()
)

#sort by descending revenue
product_revenue = product_analysis.sort_values(
    "Revenue",
    ascending=False
)

#print the top 10
top_10_products = product_revenue.head(10)
print(top_10_products)

# COMMAND ----------

#Graph

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_products["ProductName"],
    top_10_products["Revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Product Units Sold

# COMMAND ----------

product_units = product_analysis.sort_values(
    "Units",
    ascending=False
)

top_10_units = product_units.head(10)

print(top_10_units.to_string())


# COMMAND ----------

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_units["ProductName"],
    top_10_units["Units"]
)

plt.title("Top 10 Products by Units Sold")
plt.xlabel("Units Sold")
plt.ylabel("Product")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #City Revenue

# COMMAND ----------

city_analysis = (
    analysis_df
    .assign(
        City=analysis_df["City"].fillna("Uncategorized")
    )
    .groupby("City")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("OrderID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)
#sort
city_analysis = city_analysis.sort_values(
    "Revenue",
    ascending=False
)
top_10_cities = city_analysis.head(10)

print(top_10_cities)

# COMMAND ----------

#Graph

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_cities["City"],
    top_10_cities["Revenue"]
)

plt.title("Top 10 Cities by Revenue")
plt.xlabel("Revenue")
plt.ylabel("City")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Customer Segment Revenue

# COMMAND ----------

segment_analysis = (
    analysis_df
    .groupby("CustomerSegment")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("OrderID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

#Calculate Average Order Value (AOV)
segment_analysis["AOV"] = (
    segment_analysis["Revenue"] /
    segment_analysis["Orders"]
)

#Sort
segment_analysis = segment_analysis.sort_values(
    "Revenue",
    ascending=False
)

print(segment_analysis)

# COMMAND ----------

#Graph

plt.figure(figsize=(8, 5))

plt.bar(
    segment_analysis["CustomerSegment"],
    segment_analysis["Revenue"]
)

plt.title("Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue")

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Order status
# MAGIC
# MAGIC For this analysis we do not filter to Completed + Paid, because we're trying to understand the overall order status.

# COMMAND ----------

status_analysis = (
    df["Status"]
    .value_counts()
    .reset_index()
)

status_analysis.columns = [
    "Status",
    "Orders"
]

# COMMAND ----------

#Calculate the percentage

status_analysis["Percentage"] = (
    status_analysis["Orders"] /
    status_analysis["Orders"].sum()
) * 100

print(status_analysis)

# COMMAND ----------

plt.figure(figsize=(8, 8))  # A square aspect ratio works best for pie charts
plt.pie(
    status_analysis["Orders"], 
    labels=status_analysis["Status"], 
    autopct="%1.1f%%",         # Displays the percentage on each slice
    startangle=140             # Rotates the start of the pie chart for better layout
)
plt.title("Order Status")
plt.tight_layout()
plt.show()


# COMMAND ----------

# MAGIC %md
# MAGIC #Payment Status
# MAGIC
# MAGIC Same principle: use the full dataset, not the recognised-revenue dataset.

# COMMAND ----------

payment_status = (
    df["PaymentStatus"]
    .value_counts()
    .reset_index()
)

payment_status.columns = [
    "PaymentStatus",
    "Orders"
]

payment_status["Percentage"] = (
    payment_status["Orders"] /
    payment_status["Orders"].sum()
) * 100

# COMMAND ----------

#Graph
plt.figure(figsize=(8, 5))

plt.bar(
    payment_status["PaymentStatus"],
    payment_status["Orders"]
)

plt.title("Payment Status")
plt.xlabel("Payment Status")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #Payment Failure by Payment Method
# MAGIC
# MAGIC This is slightly different.
# MAGIC
# MAGIC We want:
# MAGIC
# MAGIC Failed payments ÷ total payments for each payment method

# COMMAND ----------

payment_method_analysis = (
    df
    .groupby("PaymentMethod")
    .agg(
        Total_Payments=("PaymentStatus", "count"),
        Failed_Payments=(
            "PaymentStatus",
            lambda x: (x == "Failed").sum()
        )
    )
    .reset_index()
)

#Then

payment_method_analysis["Failure_Rate"] = (
    payment_method_analysis["Failed_Payments"] /
    payment_method_analysis["Total_Payments"]
) * 100

#Sort

payment_method_analysis = payment_method_analysis.sort_values(
    "Failure_Rate",
    ascending=False
)

print(payment_method_analysis)

# COMMAND ----------

#Graph

plt.figure(figsize=(8, 8))  # Changed to a square ratio to keep the pie circular

plt.pie(
    payment_method_analysis["Failure_Rate"],
    labels=payment_method_analysis["PaymentMethod"],
    autopct="%1.1f%%",         # Displays the percentage share on each slice
    startangle=140             # Rotates the chart for a cleaner starting layout
)

plt.title("Payment Failure Rate by Payment Method")
plt.tight_layout()
plt.show()


# COMMAND ----------

# MAGIC %md
# MAGIC #Discount Analysis
# MAGIC
# MAGIC This is another analysis where we want to use the recognised-revenue dataset.

# COMMAND ----------

discount_analysis = (
    analysis_df
    .groupby("Discount")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("OrderID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

#Calculate AOV
discount_analysis["AOV"] = (
    discount_analysis["Revenue"] /
    discount_analysis["Orders"]
)

#Calculate average units per order
discount_analysis["Avg_Units_Per_Order"] = (
    discount_analysis["Units"] /
    discount_analysis["Orders"]
)

#Sort by discount
discount_analysis = discount_analysis.sort_values(
    "Discount"
)

print(discount_analysis)

# COMMAND ----------

#Graph

plt.figure(figsize=(8, 5))

plt.plot(
    discount_analysis["Discount"] * 100,
    discount_analysis["AOV"],
    marker="o"
)

plt.title("Average Order Value by Discount")
plt.xlabel("Discount (%)")
plt.ylabel("Average Order Value")

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC This supports the observation that higher discount levels generally correspond with lower AOV in this dataset, but we should not claim that discounts caused the lower AOV.

# COMMAND ----------

plt.figure(figsize=(8, 5))

plt.plot(
    discount_analysis["Discount"] * 100,
    discount_analysis["Avg_Units_Per_Order"],
    marker="o"
)

plt.title("Average Units per Order by Discount")
plt.xlabel("Discount (%)")
plt.ylabel("Average Units per Order")

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC This is useful because the business question asks whether:
# MAGIC
# MAGIC Bigger discounts lead to bigger orders, or simply lower revenue?

# COMMAND ----------

# MAGIC %md
# MAGIC #MATPLOTLIB DASHBOARD

# COMMAND ----------

#plt.subplots()

fig = plt.figure(figsize=(18, 14))

gs = fig.add_gridspec(
    3, 
    3
)

#We can display them as cards.
fig = plt.figure(figsize=(18, 12))

gs = fig.add_gridspec(
    3,
    3,
    height_ratios=[1, 2, 2]
)

#Then
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

#Make the first KPI card
ax1.text(
    0.5,
    0.5,
    f"R {total_revenue:,.2f}",
    ha="center",
    va="center",
    fontsize=22,
    fontweight="bold"
)

ax1.set_title(
    "Total Revenue",
    fontsize=14
)

ax1.axis("off")

#2nd KPI
ax2.text(
    0.5,
    0.5,
    f"{total_orders:,}",
    ha="center",
    va="center",
    fontsize=22,
    fontweight="bold"
)

ax2.set_title(
    "Total Orders",
    fontsize=14
)

ax2.axis("off")

#AOV KPI
ax3.text(
    0.5,
    0.5,
    f"R {aov:,.2f}",
    ha="center",
    va="center",
    fontsize=22,
    fontweight="bold"
)

ax3.set_title(
    "Average Order Value",
    fontsize=14
)

ax3.axis("off")

#Monthly revenue chart
monthly_revenue = (
    analysis_df
    .groupby("Year_Month")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("OrderID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)
ax4 = fig.add_subplot(gs[1, :])

ax4.plot(
    monthly_revenue["Year_Month"],
    monthly_revenue["Revenue"],
    marker="o"
)

ax4.set_title(
    "Monthly Revenue Trend",
    fontsize=16,
    fontweight="bold"
)

ax4.set_xlabel("Month")
ax4.set_ylabel("Revenue")

ax4.tick_params(axis="x", rotation=45)


#Category chart
ax5 = fig.add_subplot(gs[2, 0])

ax5.bar(
    category_analysis["Category"],
    category_analysis["Revenue"]
)

ax5.set_title(
    "Revenue by Category",
    fontweight="bold"
)

ax5.set_xlabel("Category")
ax5.set_ylabel("Revenue")

ax5.tick_params(
    axis="x",
    rotation=45
)

#Customer segement chart
ax6 = fig.add_subplot(gs[2, 1])

ax6.bar(
    segment_analysis["CustomerSegment"],
    segment_analysis["Revenue"]
)

ax6.set_title(
    "Revenue by Customer Segment",
    fontweight="bold"
)

ax6.set_xlabel("Customer Segment")
ax6.set_ylabel("Revenue")

#Order status chart
ax7 = fig.add_subplot(gs[2, 2])

ax7.bar(
    status_analysis["Status"],
    status_analysis["Orders"]
)

ax7.set_title(
    "Order Status",
    fontweight="bold"
)

ax7.set_xlabel("Status")
ax7.set_ylabel("Orders")

#fit to order
plt.tight_layout()
plt.show()