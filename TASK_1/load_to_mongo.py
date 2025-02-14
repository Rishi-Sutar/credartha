import pandas as pd
import re
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set. Check your .env file.")

def load_csv(file_path):
    """Load CSV into a Pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def clean_transaction_data(df):
    """Clean the transaction DataFrame: handle missing values, standardize date format, and transaction descriptions."""
    
    df.fillna({
        'Amount': 0, 
        'Category': 'Unknown',
        'Date': datetime.today().strftime('%Y-%m-%d')
    }, inplace=True)
    
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df.dropna(subset=['Date'], inplace=True)
    
    if 'Description' in df.columns:
        df['Description'] = df['Description'].astype(str).str.lower().apply(lambda x: re.sub(r'[^a-z0-9 ]', '', x))
    
    return df

def clean_bureau_data(df):
    """Clean the bureau DataFrame: handle missing values."""
    df.fillna({
        'Credit Score': df['Credit Score'].median(),
        'Existing Loans': 0,
        'Utilization': 0.0,
        'Missed Payments (12M)': 0,
        'Total Outstanding Debt': 0.0,
        'Debt-to-Income Ratio': 0.0
    }, inplace=True)
    
    return df

def store_in_mongodb(df, db_name, collection_name, mongo_uri=MONGO_URI):
    """Store cleaned DataFrame into MongoDB Atlas."""
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(df.to_dict(orient='records'))
        print(f"Data successfully stored in MongoDB collection: {collection_name}.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")

if __name__ == "__main__":
    transaction_file = "data/synthetic_transactions.csv"  # Update with actual path
    bureau_file = "data/synthetic_bureau.csv"
    
    try:
        transaction_df = load_csv(transaction_file)
        bureau_df = load_csv(bureau_file)

        cleaned_transaction_df = clean_transaction_data(transaction_df)
        cleaned_bureau_df = clean_bureau_data(bureau_df)

        store_in_mongodb(cleaned_transaction_df, db_name="FinancialDB", collection_name="Transactions")
        store_in_mongodb(cleaned_bureau_df, db_name="FinancialDB", collection_name="BureauReports")
    except Exception as e:
        print(f"Error: {e}")
