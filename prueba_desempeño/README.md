# 📊 Database Analysis - E-commerce

This project performs a comprehensive analysis of an e-commerce database, including SQL queries, statistical analysis, and data visualization.

## 🚀 Prerequisites

### Database

- PostgreSQL with the `test_performance` database
- The necessary tables: `customer`, `order`, `order_item`, `product`, `category`, `address`

### Environment Variables

Create a `.env` file in the project root with:

```env
DB_URL=postgresql://user:password@localhost:5432/test_performance
```

## 📦 Dependencies

Install the following libraries:

```
pip install pandas numpy sqlalchemy psycopg2-binary matplotlib seaborn python-dotenv
```
### Another way to install packages.
You can also create a requirements file for easier management and downloading. You would need to do the following:
- Create the requirement.txt file
- Add the packages you need
- Run the command ``` python -r (filename_that_contains_requirement.txt)```

## 🎯 Project Execution

1. **Configure** the environment variables in `.env`
2. **kernel** Check the kernel and choose where the packages are installed
2. **Execute** the cells in order to load the data
3. **Review** the results of each query
4. **Analyze** the generated visualizations
5. **Interpret** the insights obtained

Each section is designed to run independently, allowing for modular and flexible analysis.

## 🔧 Configuration

```
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Environment Variables
load_dotenv()
DB_URL = os.getenv('DB_URL')

# Check Connection
try:
engine = create_engine(DB_URL)
with engine.connect() as conn:
print("✅ Successful connection to database 'test_performance'")
except Exception as e:
print("❌ Error connecting:", e)
```

## 📋 Queries and Analysis

1. Loading Main Tables

```
tables = ["customer", "order", "order_item", "product", "category"]
dataframes = {}

for name in tables: 
try: 
df = pd.read_sql_table(name, con=engine) 
dataframes[name] = df 
print(f"✅ Table '{name}' loaded successfully ({len(df)} rows)") 
except Exception as e: 
print(f"⚠️ Could not load table '{name}': {e}")
```

2. Main Sales Inquiry

```


sales_query = """
SELECT 
o.id_order, 
o.created_at AS order_date, 
c.full_name AS customer_name, 
a.city AS customer_city, 
p.name AS product_name, 
cat.name AS category_name, 
oi.amount AS quantity, 
oi.price AS unit_price, 
oi.subtotal AS subtotal_item, 
SUM(oi2.subtotal) AS total_order
FROM order_item AS oi
JOIN "order" AS or ON oi.order_id = o.id_order
JOIN customer AS c ON o.customer_id = c.id_customer
JOIN address AS a ON c.address_id = a.id_address
JOIN product AS p ON oi.product_id = p.id_product
JOIN category AS cat ON p.category_id = cat.id_category
JOIN order_item AS oi2 ON oi2.order_id = o.id_order
GROUP BY 
o.id_order, o.created_at, c.full_name, a.city, 
p.name, cat.name, oi.amount, oi.price, oi.subtotal
ORDER BY o.id_order;
"""

df_sales = pd.read_sql(query_ventas, engine)
print("✅ Sales query executed successfully. Records loaded:", len(df_ventas))
```

### 3. Analysis by Dimensions

* **By City**: Total sales, number of orders, and unique customers
* **By Category**: Total sales, products sold, and total quantity
* **By Product**: Total sales, quantity sold, and average price
* **By Customer**: Number of orders and total spent

### 4. Statistical Analysis

* **Central Tendency**: Mean, median, and mode of spending per order and customer
* **Measures of Dispersion**: Variance, standard deviation, and interquartile range
* **Average Ticket**: AOV (Average Order Value) per order and customer

### 5. Rankings and Top Performers

* **Top 5 Categories** by sales
* **Top 5 Products** by quantity sold
* **Top 5 Products** by revenue
* **Product with the greatest price variability**

## 📊 Views

### 1. Histogram of Spending by Customer

```
plt.figure(figsize=(10, 6))
sns.histplot(df_gasto_cliente['gasto_total'], bins=20, kde=True, color='purple')
plt.title('Histogram of Total Spending by Customer')
plt.xlabel('Total Spending ($)')
plt.ylabel('Number of Customers')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
```

### 2. Boxplot of Sales by Category

```
plt.figure(figsize=(12, 6))
sns.boxplot(x='category_name', y='subtotal_item', data=df_ventas, palette='coolwarm')
plt.title('Sales Distribution by Category')
plt.xlabel('Category')
plt.ylabel('Sales Amount (Subtotal $)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
```

### 3. Top 5 Categories by Sales

```
plt.figure(figsize=(8, 5))
sns.barplot(x='total_sales', y='category', data=df_top5_categorias, palette='viridis')
plt.title('Top 5 Categories by Total Sales')
plt.xlabel('Total Sales ($)')
plt.ylabel('Category')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
```

### 4. Top 5 Products by Revenue

```
plt.figure(figsize=(8, 5))
sns.barplot(x='total_revenue', y='product', data=df_top5_revenue, palette='crest')
plt.title('Top 5 Products by Total Revenue')
plt.xlabel('Total Revenue ($)')
plt.ylabel('Product')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
```

## 💡 Insights and Storytelling

### 🧠 Insight 1 – Customers and Average Spending

**Evidence:**
The analysis of spending by customer showed an **uneven distribution** , with a few customers accounting for a large portion of total revenue, while the majority maintain low or moderate spending.
This is reflected in the **histogram of spending by customer** , which is concentrated toward low values ​​and has a **high standard deviation** , indicating a strong dispersion of spending.

**Recommendation:**
Implement a **loyalty or rewards program** for higher-spending customers, and encourage more frequent purchases for lower-spending customers through **personalized promotions**.

> 🎯 *This would balance spending distribution and increase the overall average ticket.*

