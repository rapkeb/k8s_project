import pandas as pd
from pymongo import MongoClient, errors, ASCENDING

# MongoDB connection settings
mongo_host = 'mongo-service'
mongo_port = 27017  # Default MongoDB port
database_name = 'churn_prediction'
collection_name = 'raw_data'

# Function to check if collection is empty
def is_collection_empty(client, db_name, coll_name):
    db = client[db_name]
    collection = db[coll_name]
    return collection.count_documents({}) == 0

# Function to load CSV data into MongoDB
def load_csv_into_mongodb(csv_file):
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    try:
        if is_collection_empty(client, database_name, collection_name):
            df = pd.read_csv('churn.csv')
            print(df.dtypes)
            data = df.to_dict(orient='records')
            result = collection.insert_many(data)
            print(f"{len(result.inserted_ids)} document(s) imported successfully.")
            create_indexes_in_mongodb(client, database_name, collection_name)
        else:
            print("Collection already contains documents. Skipping data import and index creation.")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except errors.BulkWriteError as bwe:
        print(f"Error importing data: {bwe.details['writeErrors']}")
    finally:
        client.close()

# Function to create indexes in MongoDB
def create_indexes_in_mongodb(client, db_name, coll_name):
    db = client[db_name]
    collection = db[coll_name]

    try:
        collection.create_index("customerID", unique=True)
        collection.create_index([("MonthlyCharges", ASCENDING)])
        print("Indexes created successfully.")
    except errors.OperationFailure as oe:
        print(f"Error creating indexes: {oe}")

# Main execution
if __name__ == "__main__":
    csv_file_path = 'churn.csv'  # Adjust path to your CSV file
    load_csv_into_mongodb(csv_file_path)
