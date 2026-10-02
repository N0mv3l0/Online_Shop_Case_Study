# 🛒 Shop Performance Analysis

## 📌 Project Overview

This project analyses the performance of an online shop from **January 2024 to June 2026**.

The shop sells electronics, accessories, wearables, home office products, stationery and gaming products.

The objective of this case study was to transform raw customer, order, payment and product data into clear business insights that can help the Head of Operations understand:

- How much revenue the shop generated
- How revenue changed over time
- Which products and categories performed best
- Which cities and customer segments generated the most revenue
- Order cancellations and returns
- Payment failures
- The relationship between discounts, order size and revenue

The project follows the complete data analysis workflow:

**Business Problem → Data Understanding → Data Cleaning → Data Preparation → Analysis → Visualisation → Insights → Recommendations**

---

## 🎯 Business Questions

The analysis focuses on six key business questions:

1. How much revenue did the shop make, how many orders were placed, and what was the Average Order Value (AOV)?
2. Is revenue growing, shrinking or remaining relatively flat over time?
3. Which products and categories generate the most revenue and which sell the most units?
4. Which cities and customer segments are the most valuable?
5. What proportion of orders are cancelled or returned, and what proportion of payments fail?
6. Do larger discounts result in larger orders, or do they mainly reduce revenue?

---

## 📂 Dataset

The original case study consisted of four datasets:

| Dataset | Description |
|---|---|
| `customers.csv` | Customer information |
| `orders.csv` | Order information |
| `payments.csv` | Payment attempts and payment status |
| `products.csv` | Product information |

### Key columns

**Customers**
- CustomerID
- Age
- City
- SignupDate
- CustomerSegment

**Orders**
- OrderID
- CustomerID
- OrderDate
- ProductID
- Quantity
- Discount
- PaymentMethod
- Status

**Payments**
- PaymentID
- OrderID
- PaymentDate
- PaymentStatus

**Products**
- ProductID
- ProductName
- Category
- UnitPrice

The datasets were combined using:

```text
Orders → Customers
CustomerID

Orders → Products
ProductID

Orders → Payments
OrderID
