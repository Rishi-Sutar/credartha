import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler


# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DataTransformation:
    def initiate_data_transformation(self, train_data, test_data):
        try:
            # Read train and test data
            train_df = pd.read_csv(train_data)
            test_df = pd.read_csv(test_data)
            
            logging.info("Read train and test data completed")

            # Drop unwanted columns (e.g., 'Customer ID')
            train_df.drop(columns=['Customer ID'], inplace=True, errors='ignore')
            test_df.drop(columns=['Customer ID'], inplace=True, errors='ignore')
            
            logging.info("Unwanted columns dropped")

            X_train = train_df.drop(columns=['Risk Classification'], errors='ignore')
            y_train = train_df['Risk Classification']
            X_test = test_df.drop(columns=['Risk Classification'], errors='ignore')
            y_test = test_df['Risk Classification']

            # Standard scaling
            sc = StandardScaler()
            X_train_scaled = sc.fit_transform(X_train)
            X_test_scaled = sc.transform(X_test)
            
            logging.info("Standard scaling applied to train and test data")

            # Return scaled data and target variables
            return X_train_scaled, X_test_scaled, y_train, y_test

        except Exception as e:
            logging.error(f"Data transformation failed due to {e}")
            raise Exception(f"Data transformation failed due to {e}")

if __name__ == "__main__":
    pass