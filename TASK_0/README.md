# Synthetic Financial Transactions and Credit Bureau Dataset

## Overview
This task generates a synthetic dataset for financial transactions and credit bureau reports. The dataset simulates real-world banking transactions and credit-related data, which can be used for tasks such as credit risk modeling, fraud detection, and financial behavior analysis.

## Features
The script generates two datasets:
1. **Synthetic Transactions Dataset (`synthetic_transactions.csv`)**
   - Represents financial transactions of 1,000 customers over a year.
   - Each customer has 50 transactions, resulting in a total of 50,000 records.
   - Includes various transaction categories like salary credits, shopping, food, loan payments, utility bills, cash withdrawals, and transfers.
   - Contains noisy data such as incorrect capitalization, missing values, and empty merchant names for realism.

2. **Synthetic Credit Bureau Dataset (`synthetic_bureau.csv`)**
   - Represents credit-related information for the same 1,000 customers.
   - Includes features such as credit score, number of existing loans, utilization ratio, missed payments, total outstanding debt, and debt-to-income ratio.
   - Credit scores are dynamically calculated based on financial indicators.

## Installation
To run the script, ensure you have Python installed along with the required dependencies.

### Dependencies
Install the required packages using pip:
```sh
pip install -r requirements.txt
```

## Usage
Run the script using:
```sh
python generate_synthetic_data.py
```
This will generate two CSV files in the current directory:
- `synthetic_transactions.csv`
- `synthetic_bureau.csv`

## Data Schema
### Transactions Dataset (`synthetic_transactions.csv`)
| Column Name  | Description |
|-------------|------------|
| Customer ID | Unique ID for each customer |
| Date        | Transaction date (randomized format) |
| Category    | Type of transaction |
| Source      | Merchant or transaction source |
| Amount      | Transaction amount |

### Credit Bureau Dataset (`synthetic_bureau.csv`)
| Column Name               | Description |
|---------------------------|------------|
| Customer ID               | Unique ID for each customer |
| Credit Score              | Creditworthiness score (300-900) |
| Existing Loans            | Number of current loans |
| Utilization               | Credit utilization ratio (0-1) |
| Missed Payments (12M)     | Count of missed payments in the last 12 months |
| Total Outstanding Debt    | Total debt in monetary terms |
| Debt-to-Income Ratio      | Debt burden relative to income |

## Data Quality Enhancements
The script introduces minor data inconsistencies to simulate real-world scenarios:
- **Incorrect capitalization** in transaction categories.
- **Missing values** in the transaction amounts.
- **Empty merchant names** in some transactions.

## Applications
This dataset can be used for:
- Credit risk assessment and modeling.
- Analyzing financial spending behavior.
- Fraud detection and anomaly analysis.
- Machine learning model training for financial services.

