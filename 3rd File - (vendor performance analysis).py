# =========================================
# VENDOR PERFORMANCE ANALYSIS
# =========================================
# Objective:
# Analyze vendor performance using key metrics such as
# profitability, inventory efficiency, and procurement behavior.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

server = r'ADS_G15\SQLEXPRESS'
database = 'MyprojectDatabase'
conn = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# =========================================
# LOAD DATA
# =========================================

df=pd.read_sql('select * from summary_table',conn)
#print(df)

# Exploratory Data Analysis
# -----------------------------
# ** Previously, we examined the various tables in the database to identify key variables, understand their relationships, and
# determine which ones should be included in the final analysis.
#--------------------------------------------------------------------------------------------------------------
# ** In this phase of EDA, we will analyze the resultant table to gain insights into the distribution of each column.
# This will help us understand data patterns, identify anomalies, and ensure data quality before proceeding with further analysis.

print(df.describe().T)

print('StockTurnover',df['StockTurnover'].max())
print('PurchasePrice',df['PurchasePrice'].max())
print('ActualPrice',df['ActualPrice'].max())
print('FreightCost',df['FreightCost'].max())

# Negative & Zero Values:

# **Gross Profit: Minimum value is -52,002.78, indicating losses. Some products or transactions may be selling
# at a loss due to high costs or selling at discounts lower than the purchase price.
#--------------------------------------------------------------------------------------------------------------
# **Total Sales Quantity & Sales Dollars: Minimum values are 0, meaning some products were purchased but never sold.
# These could be slow-moving or obsolete stock.

#Outliers Indicated by High Standard Deviations:

# **Purchase & Actual Prices: The max values (5,681.81 & 7,499.99) are significantly higher than
# the mean (24.39 & 35.64), indicating potential premium products.
#--------------------------------------------------------------------------------------------------------------
# **Freight Cost: Huge variation, from 0.09 to 257,032.07, suggests logistics inefficiencies or bulk shipments.
#--------------------------------------------------------------------------------------------------------------
# **Stock Turnover: Ranges from 0 to 274.5, implying some products sell extremely fast while others remain in stock indefinitely.
#--------------------------------------------------------------------------------------------------------------
# **Value more than 1 indicates that sold quantity for that product is higher than purchased quantity due to either sales being fulfilled from older stock.

# let's filter the data by removing inconsistencies
df = pd.read_sql_query("SELECT * FROM summary_table WHERE GrossProfit > 0 AND ProfitMargin > 0 AND TotalSalesQuantity > 0", conn)
print(df)

#1st Question - identify brands that need promotional or pricing adjustment which exhibit lower sales
# performance but higher profit margins

brand_performance = df.groupby('Description').agg({'TotalSalesDollars': 'sum',
'ProfitMargin': 'mean'}).reset_index()

low_sales_threshold = brand_performance['TotalSalesDollars'].quantile(0.15)
high_margin_threshold = brand_performance['ProfitMargin'].quantile(0.85)


# Filter brands with low sales but high profit margins
target_brands = brand_performance[
    (brand_performance['TotalSalesDollars'] <= low_sales_threshold) &
    (brand_performance['ProfitMargin'] >= high_margin_threshold)]

print("Brands with Low Sales but High Profit Margins:")
print(target_brands)

brand_performance=brand_performance[brand_performance['TotalSalesDollars']<1000] # for better visulization

plt.figure(figsize=(10, 6))
sns.scatterplot(data=brand_performance, x='TotalSalesDollars', y='ProfitMargin', color='blue', label="All Brands", alpha=0.2)
sns.scatterplot(data=target_brands, x='TotalSalesDollars', y='ProfitMargin', color='red', label="Target Brands")

plt.xlabel("Total Sales ($)")
plt.ylabel("Profit Margin (%)")
plt.title("Brands for Promotional or Pricing Adjustments")
plt.legend()
plt.grid(True)
plt.show()

# Insight: Identifies products with strong margins but weak sales,198 brands exhibit lower sales but higher profit margins,
# which could benefit from targeted marketing


#2nd Question - which vendors and brands demonstrate the highest sales performance?
# Top Vendors & Brands by Sales Performance
top_vendors = df.groupby("VendorName")["TotalSalesDollars"].sum().nlargest(10)
top_brands = df.groupby("Description")["TotalSalesDollars"].sum().nlargest(10)

print(top_vendors)
print(top_brands)

plt.figure(figsize=(15, 5))

# Plot for Top Vendors
plt.subplot(1, 2, 1)
ax1 = sns.barplot(y=top_vendors.index, x=top_vendors.values, palette="Blues_r")
plt.title("Top 10 Vendors by Sales")

# Plot for Top Brands
plt.subplot(1, 2, 2)
ax2 = sns.barplot(y=top_brands.index.astype(str), x=top_brands.values, palette="Reds_r")
plt.title("Top 10 Brands by Sales")

plt.tight_layout()
plt.show()

# Insight:
# Highlights highest revenue contributors


#3rd Question - which vendors contribute the most to total purchase dollar?
vendor_performance = df.groupby('VendorName').agg({
    'TotalPurchaseDollars': 'sum',
    'GrossProfit': 'sum',
    'TotalSalesDollars': 'sum'}).reset_index()

vendor_performance['PurchaseContribution%'] = (vendor_performance['TotalPurchaseDollars'] / vendor_performance['TotalPurchaseDollars'].sum())*100
print(vendor_performance.sort_values('PurchaseContribution%',ascending=False))

best_vendors=vendor_performance.sort_values('PurchaseContribution%',ascending=False).head(10)
best_vendors['PurchaseContribution%'] = best_vendors['PurchaseContribution%'].round(2)
print(best_vendors)

# Insight:
# Few vendors dominate procurement → concentration risk,

#4th Question - total procurement by top vendors

print(best_vendors['PurchaseContribution%'].sum())

best_vendors['cumulative_contribution']=best_vendors['PurchaseContribution%'].cumsum()
print(best_vendors)

# Insight:
# The top 10 vendors contribute 65.69% of total purchases

#5th Question - Does purchasing in bulk reduce unit price?
# what is the optimal purchase volume for cost saving?

df['UnitPurchasePrice'] = df['TotalPurchaseDollars'] / df['TotalPurchaseQuantity']

df['OrderSize'] = pd.qcut(df['TotalPurchaseQuantity'], q=3, labels=["Small", "Medium", "Large"])

print(df.groupby('OrderSize')['UnitPurchasePrice'].mean())

plt.figure(figsize=(10, 6))
sns.boxplot(data=df,x="OrderSize",y="UnitPurchasePrice",hue="OrderSize",palette="Set2",legend=False)
plt.title("Impact of Bulk Purchasing on Unit Price")
plt.xlabel("Order Size")
plt.ylabel("Average Unit Purchase Price")
plt.show()

# Insight:
# Vendors buying in bulk (Large Order Size) get the lowest unit price ($10.78 per unit),
# meaning higher margins if they can manage inventory efficiently.
# The price difference between Small and Large orders is substantial (~72% reduction in unit cost)
# This suggests that bulk pricing strategies successfully encourage vendors to purchase in larger volumes,
# leading to higher overall sales despite lower per-unit revenue.

#6th Question - Which vendors have low inventory turnover, indicating excess stock and slow-moving products?


print(df.groupby('VendorName')['StockTurnover'].mean().sort_values(ascending=True).head(10))

# Insight:
#Slow-moving inventory increases storage costs, reduces cash flow efficiency, and affects overall profitability.

#7th Question -How much capital is locked in unsold inventory per vendor, and which vendors contribute the most to it?

df["UnsoldInventoryValue"] = (df["TotalPurchaseQuantity"] - df["TotalSalesQuantity"]) * df["PurchasePrice"]
print('Total Unsold Capital:', df["UnsoldInventoryValue"].sum())

# Aggregate Capital Locked per Vendor
inventory_value_per_vendor = df.groupby("VendorName")["UnsoldInventoryValue"].sum().reset_index()

# Sort Vendors with the Highest Locked Capital
inventory_value_per_vendor = inventory_value_per_vendor.sort_values(by="UnsoldInventoryValue", ascending=False).head(10)
print(inventory_value_per_vendor)

# Insight:
#Total Unsold Inventory Capital: $2.71M ,High unsold inventory ($2.71M) is concentrated among a few vendors
#This ties up capital and increases holding costs.