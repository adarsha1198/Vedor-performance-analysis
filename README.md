[Open Google Drive Dataset](https://drive.google.com/drive/folders/1AYgk6MmTGYJSGhal3hfwkyGzHkSdwc_T?usp=sharing)    
#  Vendor Performance Analysis | End-to-End Business Intelligence Project

##  Overview
This project analyzes vendor performance by building a complete data pipeline from raw data ingestion to business insights and dashboarding.  

The objective is to evaluate vendor profitability, inventory efficiency, procurement effectiveness, and pricing strategies to support better business decisions.

---

##  Business Problem
How can a company evaluate and optimize vendor performance to improve profitability, reduce inventory inefficiencies, and enhance procurement decisions?

---

##  Workflow
Data Ingestion → Data Cleaning & Feature Engineering → Business Analysis → Power BI Dashboard  

---

##  Tech Stack
- Python (Pandas, NumPy, Matplotlib, Seaborn)  
- SQL Server (T-SQL: Joins, Aggregations, CTEs)  
- SQLAlchemy  
- Power BI  

---

##  Analysis Covered

###  Data Processing
- Integrated multiple datasets: Purchases, Sales, Inventory, Vendor Invoices, Pricing  
- Built a centralized analytical table (`summary_table`)  
- Performed data cleaning, consistency checks, and outlier handling  

###  Key Metrics Created
- Gross Profit  
- Profit Margin (%)  
- Stock Turnover  
- Sales-to-Purchase Ratio  

###  Business Analysis
- Vendor and product profitability analysis  
- Inventory efficiency and stock turnover evaluation  
- Procurement and pricing impact analysis  
- Vendor contribution and ranking  
- Identification of excess inventory and capital lock-in  

---

##  Key Insights
- High-margin products often have low sales → potential for targeted promotion  
- Bulk purchasing reduces unit cost but may lead to overstocking  
- Certain vendors contribute disproportionately to procurement  
- Low inventory turnover indicates capital locked in unsold stock  
- Freight cost variability suggests operational inefficiencies  

---

##  Dashboard
A Power BI dashboard built on the `summary_table` provides:
- Vendor performance tracking  
- Profitability analysis  
- Inventory insights  
- Sales trends  

---

##  Outcome
This project demonstrates how raw transactional data can be transformed into actionable insights to support vendor selection, inventory optimization, and cost-efficient procurement strategies.
