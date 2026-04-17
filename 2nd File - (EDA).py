# =========================================
# DATA PROCESSING & FEATURE ENGINEERING
# =========================================
# Objective:
# Integrate multiple datasets and create a centralized analytical table
# for vendor performance analysis.

from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text
import numpy as np

# =========================================
# DATABASE CONNECTION
# =========================================

server = r'ADS_G15\SQLEXPRESS'
database = 'MyprojectDatabase'

conn = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# =========================================
# DATA UNDERSTANDING
# =========================================
# Extracting data from different tables for a specific vendor
# to understand structure and relationships


tables = pd.read_sql("SELECT name FROM sys.tables", conn)
print(tables)
for table in tables['name']:
    print("-"*50,table,"-"*50)
    print("count of records:-",pd.read_sql(f'select count(*) as count from {table}',conn)['count'].values[0])
    print(pd.read_sql(f'select top 8 * from {table} ',conn))

purchases = pd.read_sql("select * from purchases where VendorNumber=4466",conn)
print(purchases)

purchasePrices=pd.read_sql("select * from purchase_prices where VendorNumber=4466",conn)
print(purchasePrices)

vendorInvoice=pd.read_sql("select * from vendor_invoice where VendorNumber=4466",conn)
print(vendorInvoice)

Sales=pd.read_sql("select * from sales where VendorNo=4466",conn)
print(Sales)

print(purchases.groupby(['Brand','PurchasePrice'])[['Quantity','Dollars']].sum())

print(vendorInvoice['PONumber'].nunique())
print(vendorInvoice.shape)


# =========================================
# BUSINESS UNDERSTANDING (IMPORTANT)
# =========================================
# - Purchases → Vendor buying activity
# - Purchase Prices → Product pricing details
# - Vendor Invoice → Includes freight costs
# - Sales → Revenue generated from products
#
# Goal:
# Combine all these datasets into one unified table

# =========================================
# DATA AGGREGATION
# =========================================
# Freight cost per vendor

# The purchases table contains actual purchase data, including the date of purchase,
# products (brands) purchased by vendors, the amount paid (in dollars), and the quantity purchased.
#-------------------------------------------------------------------------------------------------------------
# The purchase price column is derived from the purchase_prices table, which provides product-wise actual and purchase prices.
#-------------------------------------------------------------------------------------------------------------
# The combination of vendor and brand is unique in this table.
#-------------------------------------------------------------------------------------------------------------
# The vendor_invoice table aggregates data from the purchases table,
# summarizing quantity and dollar amounts, along with an additional column for freight.
#-------------------------------------------------------------------------------------------------------------
# This table maintains uniqueness based on vendor and PO number.
#-------------------------------------------------------------------------------------------------------------
# The sales table captures actual sales transactions, detailing the brands purchased by vendors, the quantity sold, the selling price, and the revenue earned.
#-------------------------------------------------------------------------------------------------------------
# As the data that we need for analysis is distributed in different tables, we need to create a summary table containing:
#
# purchase transactions made by vendors
# sales transaction data
# freight costs for each vendor
# actual product prices from vendors

freightSummary=pd.read_sql("select VendorNumber,Sum(freight)as FreightCost from vendor_invoice group by VendorNumber",conn)
print(freightSummary)

Purchase_PurchasePrice = pd.read_sql("""
SELECT
    p.VendorNumber,
    p.VendorName,
    p.Brand,
    MAX(p.PurchasePrice) AS PurchasePrice,   -- 👈 simple fix
    pp.Volume,
    pp.Price AS ActualPrice,
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
FROM purchases p
LEFT JOIN purchase_prices pp
    ON p.Brand = pp.Brand
where p.PurchasePrice>0     
GROUP BY 
    p.VendorNumber,
    p.VendorName,
    p.Brand,
    pp.Volume,
    pp.Price
ORDER BY TotalPurchaseDollars 
""", conn)
print(Purchase_PurchasePrice)

salesSummary=pd.read_sql_query("""SELECT
    VendorNo,
    Brand,
    SUM(SalesDollars) as TotalSalesDollars,
    SUM(SalesPrice) as TotalSalesPrice,
    SUM(SalesQuantity) as TotalSalesQuantity,
    SUM(ExciseTax) as TotalExciseTax
FROM sales
GROUP BY VendorNo, Brand
ORDER BY TotalSalesDollars""", conn)
print(salesSummary)

# =========================================
# SUMMARY TABLE CREATION (CORE PART)
# =========================================
# Combines purchases, sales, and freight data into one table

summary_table=pd.read_sql("""with freightSummary as(select VendorNumber,Sum(freight)as FreightCost from vendor_invoice group by VendorNumber),
                          Purchase_PurchasePrice as(SELECT
    p.VendorNumber,
    p.VendorName,
    p.Brand,
    p.description,
    p.PurchasePrice, 
    pp.Volume,
    pp.Price AS ActualPrice,
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
FROM purchases p
LEFT JOIN purchase_prices pp
    ON p.Brand = pp.Brand
where p.PurchasePrice>0     
GROUP BY 
    p.VendorNumber,
    p.VendorName,
    p.Brand,
    pp.Volume,
    pp.Price,
    p.description,
    p.PurchasePrice),
 SalesSummary as (SELECT
    VendorNo,
    Brand,
    SUM(SalesDollars) as TotalSalesDollars,
    SUM(SalesPrice) as TotalSalesPrice,
    SUM(SalesQuantity) as TotalSalesQuantity,
    SUM(ExciseTax) as TotalExciseTax
FROM sales
GROUP BY VendorNo, Brand) 

SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM Purchase_PurchasePrice ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN freightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""",conn)
print(summary_table)

# This query generates a vendor-wise sales and purchase summary, which is valuable for:
#
# Performance Optimization:
#
# The query involves heavy joins and aggregations on large datasets like sales and purchases.
# Storing the pre-aggregated results avoids repeated expensive computations.
# Helps in analyzing sales, purchases, and pricing for different vendors and brands.
# Future benefits of storing this data for faster dashboarding & reporting.
# Instead of running expensive queries each time, dashboards can fetch data quickly from vendor_sales_summary.

# =========================================
# DATA CLEANING
# =========================================

print(summary_table.dtypes)
print(summary_table.isnull().sum())
print(summary_table['VendorName'].unique())
print(summary_table['Description'].unique())

summary_table['Volume'] = summary_table['Volume'].astype('float64')
summary_table.fillna(0, inplace=True)
summary_table['VendorName'] = summary_table['VendorName'].str.strip()
summary_table['ProfitMargin'] = summary_table['ProfitMargin'].replace([np.inf, -np.inf], 0)

print(summary_table.dtypes)
print(summary_table.isnull().sum())
print(summary_table['VendorName'].unique())

# =========================================
# FEATURE ENGINEERING (KEY METRICS)
# =========================================

summary_table['GrossProfit'] = summary_table['TotalSalesDollars'] - summary_table['TotalPurchaseDollars']
summary_table['ProfitMargin'] = (summary_table['GrossProfit'] / summary_table['TotalSalesDollars']) * 100
summary_table['StockTurnover'] = summary_table['TotalSalesQuantity'] / summary_table['TotalPurchaseQuantity']
summary_table['SalesToPurchaseRatio'] = summary_table['TotalSalesDollars'] / summary_table['TotalPurchaseDollars']

summary_table['ProfitMargin'] =summary_table['ProfitMargin'].round(2)
summary_table['StockTurnover']=summary_table['StockTurnover'].round(2)
summary_table['SalesToPurchaseRatio']=summary_table['SalesToPurchaseRatio'].round(2)



summary_table['ProfitMargin'] = summary_table['ProfitMargin'].replace([np.inf, -np.inf], 0)

# =========================================
# STORE FINAL TABLE
# =========================================
# Persisting processed data for reporting & dashboarding

with conn.begin() as connection:
    connection.execute(text("""
    CREATE TABLE summary_table (
    VendorNumber INT,
    VendorName VARCHAR(100),
    Brand INT,
    Description VARCHAR(100),
    PurchasePrice DECIMAL(10,2),
    ActualPrice DECIMAL(10,2),
    Volume DECIMAL(10,2),
    TotalPurchaseQuantity INT,
    TotalPurchaseDollars DECIMAL(15,2),
    TotalSalesQuantity INT,
    TotalSalesDollars DECIMAL(15,2),
    TotalSalesPrice DECIMAL(15,2),
    TotalExciseTax DECIMAL(15,2),
    FreightCost DECIMAL(15,2),
    GrossProfit DECIMAL(15,2),
    ProfitMargin DECIMAL(15,2),
    StockTurnover DECIMAL(15,2),
    SalesToPurchaseRatio DECIMAL(15,2),
    PRIMARY KEY (VendorNumber, Brand)
);
"""))

summary_table.to_sql('summary_table',conn,if_exists='append',index=False)
print(pd.read_sql('select * from summary_table',conn))

# =========================================
# OUTPUT
# =========================================
# summary_table is now ready for analysis and Power BI dashboard