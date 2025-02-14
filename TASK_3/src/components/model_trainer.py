import logging
import joblib
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ModelTrainer:
    def __init__(self, experiment_name="Credit Risk Assessment"):
        self.models = {
            "Logistic Regression": (LogisticRegression(random_state=42), {
                "C": [0.01, 0.1, 1, 10, 100],
                "max_iter": [500, 1000, 2000]
            }),
            "Random Forest": (RandomForestClassifier(random_state=42), {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 5, 10]
            }),
            "Neural Network": (MLPClassifier(random_state=42), {
                "hidden_layer_sizes": [(32,), (64, 32), (128, 64, 32)],
                "activation": ["relu", "tanh"],
                "max_iter": [200, 500, 1000]
            })
        }
        self.best_model = None
        self.best_score = 0
        self.best_model_name = ""
        mlflow.set_experiment(experiment_name)

    def train_and_evaluate(self, X_train, y_train, X_test, y_test, cv=3, n_iter=10):
        """Train models using RandomizedSearchCV, track results in MLflow, and save the best model."""
        try:
            results = {}

            for name, (model, param_grid) in self.models.items():
                with mlflow.start_run(run_name=f"{name} (RandomizedSearch)"):
                    logging.info(f"Training {name} with RandomizedSearchCV...")
                    
                    # Hyperparameter tuning
                    random_search = RandomizedSearchCV(model, param_grid, n_iter=n_iter, cv=cv, scoring='f1_weighted', n_jobs=-1, random_state=42)
                    random_search.fit(X_train, y_train)

                    # Get the best model from RandomizedSearchCV
                    best_model = random_search.best_estimator_

                    # Predictions
                    y_pred = best_model.predict(X_test)

                    # Evaluation metrics
                    accuracy = accuracy_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred, average='weighted')

                    results[name] = {"accuracy": accuracy, "f1_score": f1}
                    logging.info(f"{name}: Best Params = {random_search.best_params_}, Accuracy = {accuracy:.4f}, F1-score = {f1:.4f}")

                    # Log best parameters, metrics, and model in MLflow
                    mlflow.log_params(random_search.best_params_)
                    mlflow.log_metric("accuracy", accuracy)
                    mlflow.log_metric("f1_score", f1)
                    mlflow.sklearn.log_model(best_model, name)

                    # Update the best model based on F1-score
                    if f1 > self.best_score:
                        self.best_score = f1
                        self.best_model = best_model
                        self.best_model_name = name

            # Save the best model locally and in MLflow
            if self.best_model:
                joblib.dump(self.best_model, "best_model.pkl")
                logging.info(f"Best Model: {self.best_model_name} (F1-score: {self.best_score:.4f}) saved successfully!")

                # Log the best model in MLflow
                with mlflow.start_run(run_name="Best Model Selection"):
                    mlflow.log_param("best_model", self.best_model_name)
                    mlflow.log_metric("best_f1_score", self.best_score)
                    mlflow.sklearn.log_model(self.best_model, "best_model")

            return results, self.best_model_name

        except Exception as e:
            logging.error(f"Model training failed due to: {e}")
            raise

if __name__ == "__main__":
    pass
