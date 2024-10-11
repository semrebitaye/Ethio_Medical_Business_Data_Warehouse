import pandas as pd
import os
from sqlalchemy import create_engine

def clean_data(file_path):
    """
    Clean the raw data from CSV files.

    Parameters:
    - file_path: Path to the raw CSV file.

    Returns:
    - cleaned_data: DataFrame containing cleaned data.
    """
    # Load data from CSV file
    data = pd.read_csv(file_path)

    # Remove duplicates
    data = data.drop_duplicates()

    # Handle missing values
    data['message'] = data['message'].fillna('')

    # Standardize formats
    data['message'] = data['message'].str.lower()

    # Validate data
    # Example: Convert 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Drop rows with invalid dates
    data = data.dropna(subset=['date'])

    return data

def store_data_to_postgres(df, table_name, engine):
    """
    Store cleaned data to PostgreSQL database.

    Parameters:
    - df: DataFrame containing cleaned data.
    - table_name: Name of the table to store data in.
    - engine: SQLAlchemy engine instance connected to PostgreSQL.
    """
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data stored in table {table_name}")

if __name__ == '__main__':
    # Database connection details
    DATABASE_URI = 'postgresql://postgres:new_password@localhost:5432/postgres'

    # Input and output directories
    input_dir = '/home/semre/Ethio_Medical_Business_Data_Warehouse/scraping/data/raw'
    output_dir = '/home/semre/Ethio_Medical_Business_Data_Warehouse/cleaning_and_transforming/data/cleaned_transformed'

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create database engine
    engine = create_engine(DATABASE_URI)

    # Process each raw CSV file
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)
            
            # Clean the data
            cleaned_data = clean_data(input_file_path)

            # Save cleaned data to a new CSV file
            cleaned_data.to_csv(output_file_path, index=False)
            print(f"Cleaned data saved to {output_file_path}")

            # Store cleaned data to PostgreSQL
            table_name = file_name.split('.')[0]  # Use file name (without extension) as table name
            store_data_to_postgres(cleaned_data, table_name, engine)