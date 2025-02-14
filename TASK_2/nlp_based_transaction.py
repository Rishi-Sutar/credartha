import pandas as pd
import re
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib

# Load the dataset
file_path = "data/synthetic_transactions.csv"
df = pd.read_csv(file_path)

# Preprocessing function
def preprocess_text(text):
    text = str(text).lower()  # Convert to string and lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

df['clean_text'] = df['Source'].apply(preprocess_text)

# Feature Engineering using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['clean_text'])
y = df['Category']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training using RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model and vectorizer
joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

# Model Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# API Deployment with FastAPI
app = FastAPI()

class TransactionRequest(BaseModel):
    transaction: str

@app.post("/predict")
def predict_category(request: TransactionRequest):
    # Load the model and vectorizer
    model = joblib.load('random_forest_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    
    clean_text = preprocess_text(request.transaction)
    features = vectorizer.transform([clean_text])
    prediction = model.predict(features)[0]
    return {"category": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
