# Transaction and Credit Bureau Data Processing

## Overview

This script loads, cleans, and stores transaction and credit bureau data into a MongoDB database. It processes synthetic financial data, standardizes it, and ensures that missing values are handled before inserting the records into MongoDB.

## Features

- Loads transaction and credit bureau data from CSV files.
- Cleans data by handling missing values, standardizing date formats, and normalizing text.
- Stores processed data into a MongoDB database.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python packages (listed in `requirements.txt`)
- A MongoDB database (Atlas or local instance)

## Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Add the following:
     ```
     MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
     ```

## Usage

Run the script to process and store the data:

```sh
python process_data.py
```

## Data Cleaning Steps

- **Transactions Data:**

  - Fills missing values in `Amount`, `Category`, and `Date`.
  - Standardizes date format to `YYYY-MM-DD`.
  - Normalizes `Description` by converting to lowercase and removing special characters.

- **Bureau Data:**

  - Fills missing values in `Credit Score` with the median.
  - Defaults `Existing Loans`, `Utilization`, `Missed Payments (12M)`, `Total Outstanding Debt`, and `Debt-to-Income Ratio` to 0 if missing.

## Database Structure

The data is stored in a MongoDB database named `FinancialDB` with the following collections:

- `Transactions`
- `BureauReports`

## Error Handling

- If the CSV file is not found, an error is raised.
- If `MONGO_URI` is missing, execution stops with an appropriate message.
- Errors during MongoDB insertion are logged.

