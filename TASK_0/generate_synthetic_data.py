import pandas as pd
import numpy as np
from faker import Faker
import random
from typing import List

fake = Faker()
Faker.seed(42)
np.random.seed(42)

# Total transactions = 1000 * 50 = 50000
no_customers = 1000
transacton_per_customer = 50

#-------------- Creata a synthetic dataset for transactions --------------

# Categories of transactions
categories = [
    "Salary Credit", "Shopping", "Food & Dining", "Loan EMI Payment", "Utility Bill", "Cash Withdrawals", "Transfers"
]

# Sources of transactions
sources = {
    "Shopping": ["Amazon", "Flipkart", "Myntra"],
    "Food & Dining": ["Swiggy", "Zomato", "Starbucks"],
    "Loan EMI Payment": ["HDFC Loan", "SBI Home Loan", "ICICI EMI"],
    "Utility Bill": ["Electricity", "Water", "Broadband", "Gas"],
    "Cash Withdrawal": ["ATM", "Bank"],
    "Transfer": ["UPI", "IMPS", "NEFT"],
}

# Generate transactions for a customer
def generate_transactions(customer_id) -> List[List]:
    transactions = []
    
    for i in range(transacton_per_customer):
        category = np.random.choice(categories)
        source = np.random.choice(sources.get(category, [category]))
        amount = round(random.uniform(50, 5000), 2) if category != "Salary Credit" else round(random.uniform(30000, 100000), 2)
        date_format = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%b %d, %Y"])
        date = fake.date_between(start_date="-1y", end_date="today").strftime(date_format)
        transactions.append([customer_id, date, category, source, amount])
    return transactions

# Generate transactions for all customers
data = []
for customer_id in range(1, no_customers + 1):
    data.extend(generate_transactions(customer_id))

df_transactions = pd.DataFrame(data, columns=[ "Customer ID", "Date", "Category", "Source", "Amount"])

# Introduce messy data
df_transactions.loc[random.sample(range(len(df_transactions)), 10), "Category"] = "credit"  # Incorrect capitalization
df_transactions.loc[random.sample(range(len(df_transactions)), 10), "Amount"] = np.nan  # Missing values
df_transactions.loc[random.sample(range(len(df_transactions)), 10), "Source"] = ""  # Empty merchant

df_transactions.to_csv("synthetic_transactions.csv", index=False)

#-------------- Creata a synthetic dataset for Credit Bureau Report dataset --------------

# Credit Bureau Report Data
bureau_data = []
for customer_id in range(1, no_customers + 1):
    existing_loans = random.randint(0, 5)
    utilization = round(random.uniform(0, 1), 2)
    missed_payments = random.randint(0, 6) if existing_loans > 0 else 0
    total_outstanding_debt = round(random.uniform(1000, 500000), 2)
    debt_to_income_ratio = round(random.uniform(0.1, 0.8), 2)
    
    # Determine credit score dynamically
    credit_score = 900  # Start with max score
    if existing_loans > 2:
        credit_score -= 50  # More loans can impact score
    if utilization > 0.5:
        credit_score -= 100  # High utilization lowers score
    if missed_payments > 0:
        credit_score -= missed_payments * 30  # Each missed payment reduces score
    if total_outstanding_debt > 250000:
        credit_score -= 50  # High debt impacts score
    if debt_to_income_ratio > 0.5:
        credit_score -= 50  # High DTI indicates financial stress
    
    # Ensure score remains within range (300-900)
    credit_score = max(300, min(credit_score, 900))
    
    bureau_data.append([customer_id, credit_score, existing_loans, utilization, missed_payments, total_outstanding_debt, debt_to_income_ratio])

df_bureau = pd.DataFrame(bureau_data, columns=[
    "Customer ID", "Credit Score", "Existing Loans", "Utilization", "Missed Payments (12M)", "Total Outstanding Debt", "Debt-to-Income Ratio"
])

df_bureau.to_csv("synthetic_bureau.csv", index=False)

print("Synthetic dataset generated successfully!")