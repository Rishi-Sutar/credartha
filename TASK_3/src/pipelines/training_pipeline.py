from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ml_pipeline():
    ''''Define the pipeline'''
    
    # data ingestion
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    # data transformation
    data_transformation = DataTransformation()
    X_train_scaled, X_test_scaled, y_train, y_test = data_transformation.initiate_data_transformation(train_data, test_data)
    
    # model training
    trainer = ModelTrainer()
    trainer.train_and_evaluate(X_train_scaled, y_train, X_test_scaled, y_test)
    
if __name__ == "__main__":
    ml_pipeline()