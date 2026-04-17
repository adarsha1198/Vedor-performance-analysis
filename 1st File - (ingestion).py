# =========================================
# DATA INGESTION PIPELINE
# =========================================
# Objective:
# Load raw CSV files into SQL Server and create structured tables
# for downstream analysis.
import os
import pandas as pd
from sqlalchemy import create_engine
import urllib

# =========================================
# CONFIGURATION
# =========================================
# Define file path and database connection details


folder_path = r'C:\Users\adars\Downloads\data project\data'

server = 'ADS_G15\\SQLEXPRESS'
database = 'MyprojectDatabase'


driver = 'ODBC Driver 17 for SQL Server'


# =========================================
# CREATE DATABASE CONNECTION
# =========================================
# Establish connection to SQL Server using SQLAlchemy


params = urllib.parse.quote_plus(
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# =========================================
# LOAD CSV FILES INTO DATABASE
# =========================================
# Loop through all CSV files and load them as tables


for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        print(f"Reading file: {file_name}")

# Clean table name (remove spaces & special characters)

        df = pd.read_csv(file_path)


        table_name = os.path.splitext(file_name)[0]


        table_name = table_name.replace(' ', '_').replace('-', '_')

# Load into SQL Server
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        print(f"Loaded '{file_name}' into table '{table_name}'")

print("All CSV files loaded successfully!")

# =========================================
# OUTPUT
# =========================================
# Raw datasets are now available in SQL Server as structured tables