# NLP-Based Transaction Categorization

This project implements a machine learning model to classify bank transactions into predefined categories using Natural Language Processing (NLP). The model is trained using a synthetic transaction dataset and deployed as a REST API using FastAPI.

## Features

- Preprocesses transaction descriptions
- Extracts features using TF-IDF vectorization
- Trains a RandomForestClassifier for transaction classification
- Deploys the model as an API using FastAPI
- Predicts transaction categories based on input descriptions

## Installation

Ensure you have Python installed. Install the required dependencies using:

```bash
pip install -r requirements.txt
```

### Dependencies

- pandas
- numpy
- scikit-learn
- spacy
- fastapi
- uvicorn
- joblib

## Dataset

The dataset is expected to be stored at `data/synthetic_transactions.csv` and should contain:

- `Source`: Transaction descriptions
- `Category`: Corresponding category labels

## Training the Model

Run the following command to train the model and save it:

```bash
python nlp_based_transaction.py
```

This will:

- Preprocess the text
- Vectorize the data using TF-IDF
- Train a RandomForestClassifier
- Save the trained model and vectorizer using `joblib`
- Running the API

The API will be available at `http://localhost:8000/`

## API Usage

### Predict Transaction Category

#### Endpoint

```http
POST /predict
```

#### Request Body

```json
{
  "transaction": "Walmart grocery shopping"
}
```

#### Response

```json
{
  "category": "Groceries"
}
```

## Evaluation

After training, the model is evaluated using a test set, and a classification report is generated.

## Future Improvements

- Experiment with deep learning models (BERT, FastText, etc.)
- Improve preprocessing using SpaCy
- Implement real-time data updates
- Deploy as a cloud service (Azure, AWS, etc.)

