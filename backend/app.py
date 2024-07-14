from flask import Flask, jsonify
import pandas as pd
from pymongo import MongoClient


app = Flask(__name__)

try:
    # Adjust the connection string as per your Kubernetes setup
    client = MongoClient('mongo-service:27017')
    # List all databases
    print(f"Available databases: {client.list_database_names()}")
    # Use a specific database
    db = client.churn_prediction
    # List collections in the database
    print(f"Collections in churn_prediction: {db.list_collection_names()}")
    # Use a specific collection
    collection = db.raw_data
    # Example query
    print(f"First document in raw_data: {collection.find_one()}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")


@app.route('/submit/<user_id>', methods=['GET'])
def submit(user_id):
    # Query MongoDB for the specific user
    user = collection.find_one({"customerID": user_id})

    if user:
        user.pop('_id')  # Remove MongoDB's internal ID field if needed
        return jsonify(user)
    else:
        return jsonify({"error": f"User ID {user_id} not found"}), 404

    
@app.route('/upload', methods=['POST'])
def upload_csv():
    df = pd.read_csv('churn.csv')
    print(df.head)
    data = df.to_dict(orient='records')
    result = collection.insert_many(data)
    return jsonify({'result': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 201
    

@app.route('/flask/kinan', methods=['Get'])
def get_kinan():
    return f'The current time is: kinan'


if __name__ == '__main__':
    app.run(debug=True, port=5005)
