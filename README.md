# Vendor Performance Analysis
### Project Overview
[Open Google Drive File]([https://drive.google.com/your-file-link](https://drive.google.com/drive/folders/1AYgk6MmTGYJSGhal3hfwkyGzHkSdwc_T?usp=sharing))
This project analyzes vendor performance by building a structured data pipeline from raw data ingestion to business insights and dashboarding.  

The objective is to evaluate:  

Vendor profitability  
Sales performance  
Inventory efficiency  
Pricing strategies  
Procurement effectiveness  
### Project Workflow

Data Ingestion → Data Cleaning & Feature Engineering → Business Analysis → Power BI Dashboard  

### Tech Stack  
Python: Pandas, NumPy, Seaborn, Matplotlib  
SQL Server: T-SQL (Joins, Aggregations, CTEs)  
SQLAlchemy       
Power BI  
### Project Breakdown
### 1️ Data Ingestion
Loaded multiple CSV files into SQL Server  
Automated table creation based on file names  
Designed a scalable ingestion pipeline  
### 2️ Data Cleaning & Feature Engineering (EDA Phase)
Integrated multiple datasets:    
*Purchases      
*Sales     
*Begin inventory  
*end inventory  
*Vendor invoices (freight)  
*Purchase prices  
Built a central analytical table (summary_table)  
Performed:   
Data cleaning (null handling, datatype fixes)   
Outlier detection  
Data consistency checks  
Created key business metrics:  
Gross Profit  
Profit Margin (%)   
Stock Turnover  
Sales-to-Purchase Ratio  
Stored processed data in SQL for efficient querying   
### 3️ Business Analysis & Visualization
Performed analysis using Seaborn and Matplotlib  
### Key Analyses:  
Identified low-sales but high-profit products  
Ranked top vendors and brands  
Measured vendor contribution to procurement  
Analyzed impact of bulk purchasing on pricing  
Detected low inventory turnover  
Calculated capital locked in unsold inventory  
### Key Insights
High-margin products have low sales → promotion opportunity  
Bulk purchasing reduces unit cost significantly  
Some vendors hold excess inventory  
Freight cost variability indicates inefficiencies  
Few vendors dominate procurement  
### Power BI Dashboard
Built using summary_table   
Provides:  
Vendor performance insights  
Profitability tracking   
Inventory analysis   
Sales trends  
