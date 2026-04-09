#  Vendor Performance Analysis
###  Project Overview

This project analyzes vendor performance by building an end-to-end data project from raw data ingestion to business intelligence reporting.

### The goal is to evaluate:

### Vendor profitability
  Sales performance
  Inventory efficiency
  Pricing strategies
  Procurement optimization
###  Project Workflow
  Data Ingestion → Exploratory Data Analysis → Data Transformation & Analysis → Power BI Dashboard
  Tech Stack
  Python: Pandas, NumPy, Matplotlib, Seaborn
  SQL Server: T-SQL (Joins, Aggregations, CTEs)
  SQLAlchemy 
  Power BI
###  Project Breakdown
### 1️ Data Ingestion
  Loaded multiple CSV files into SQL Server
  Automatically created tables from file names
  Built a scalable ingestion pipeline for structured data
### 2️ Exploratory Data Analysis (EDA)
  Analyzed data distributions and summary statistics
  Identified:
  Missing values
  Outliers
  Negative profit cases
  Unsold inventory (zero sales)
  Built a central analytical table (summary_table)
  Created key business metrics:
  Gross Profit
  Profit Margin (%)
  Stock Turnover
  Sales-to-Purchase Ratio
  Stored processed data in SQL for efficient querying and reporting
### 3️ Data Analysis
  Integrated multiple datasets:
  Purchases
  Sales
  Vendor invoices (freight)
  Purchase prices

###  Business Problems Solved
###  Low Sales but High Profit Products
  Identified products with high margins but low sales
  Suggested opportunity for targeted promotions
###  Top Vendors & Brands
  Ranked vendors and products based on total sales
  Identified key revenue contributors
###  Vendor Contribution Analysis
  Calculated each vendor’s contribution to total procurement
  Highlighted top-performing vendors
###  Bulk Purchasing Impact
  Analyzed relationship between order size and unit price
  Found that larger orders significantly reduce cost per unit
###  Inventory Efficiency
  Identified vendors with low stock turnover
  Indicated slow-moving or excess inventory
###  Capital Locked in Inventory
  Measured unsold inventory value per vendor
  Highlighted vendors contributing most to tied-up capital
###  Key Insights
  High-margin products are underperforming in sales → promotion opportunity
  Bulk purchasing significantly reduces unit cost
  Some vendors maintain excess inventory → inefficiency
  Freight costs vary widely → scope for optimization
  A small group of vendors drives most procurement
###  Power BI Dashboard
  Built on top of the processed summary_table
  Provides:
  Vendor performance analysis
  Profitability tracking
  Inventory insights
  Sales trends
