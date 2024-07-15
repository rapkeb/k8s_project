from flask import Flask, jsonify
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


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


def convert_objectid(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@app.route('/show/<type>', methods=['GET'])
def show(type):
    if type == 'head':
        # Retrieve the first 5 documents
        documents = collection.find().limit(5)
    elif type == 'tail':
        # Retrieve the last 5 documents
        documents = collection.find().sort([('$natural', -1)]).limit(5)
    # Convert documents to JSON
    json_output = [convert_objectid(doc) for doc in documents]

    return jsonify(json_output)


@app.route('/submit/<user_id>', methods=['GET'])
def submit(user_id):
    # Query MongoDB for the specific user
    user = collection.find_one({"customerID": user_id})

    if user:
        user.pop('_id')  # Remove MongoDB's internal ID field if needed
        return jsonify(user)
    else:
        return jsonify({"error": f"User ID {user_id} not found"}), 404
    

@app.route('/charges/<monthly_charges>', methods=['GET'])
def submit_by_charges(monthly_charges):
    # Query MongoDB for customers with MonthlyCharges above the specified amount
    customers = collection.find({"MonthlyCharges": {"$gt": float(monthly_charges)}}).limit(15)
    customer_ids = [str(customer["customerID"]) for customer in customers]

    if customer_ids:
        return jsonify(customer_ids)
    else:
        return jsonify({"error": f"No customers found with MonthlyCharges above {monthly_charges}"}), 404

    
@app.route('/upload', methods=['GET'])
def upload_csv():
    df = pd.read_csv('churn.csv')
    data = df.to_dict(orient='records')
    result = collection.insert_many(data)
    return jsonify({'result': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5005)
