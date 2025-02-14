import pandas as pd

def classify_risk(row):
    if (row['Credit Score'] < 650 or row['Missed Payments (12M)'] >= 3 or 
        row['Utilization'] > 0.7 or row['Debt-to-Income Ratio'] > 0.6):
        return 'High Risk'
    else:
        return 'Low Risk'

# Load dataset from CSV
file_path = 'data/synthetic_bureau.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

df['Risk Classification'] = df.apply(classify_risk, axis=1)

df.to_csv('data/synthetic_bureau_risk.csv', index=False)
