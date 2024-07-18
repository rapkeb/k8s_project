from flask import Flask, json, jsonify, request
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
import pickle


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

    
# Function to check if collection is empty
def is_collection_empty():
    empty = collection.count_documents({}) == 0
    return empty

@app.route('/upload', methods=['GET'])
def upload_csv():
    if is_collection_empty():
        return jsonify({'result': 'No data loaded yet. Pod for loading data not completed.'}), 404
    else:
        return jsonify({'result': 'Data already inserted successfully.'}), 200
    

def writeToDB(predObj, churn):
    clients_collection = db.clients_churn
    client_data = parse_object(predObj)
    client_data['Churn'] =  churn
    clients_collection.insert_one(client_data)



@app.route('/predict', methods = ['POST'])
def predict():
    # load the data
    predObj = request.args
    # parse the data
    data = parse_object(predObj)
    #list the data
    client_data = list(data.values())
    # predict
    #load the model
    with open('model.pkl', 'rb') as f: 
        model = pickle.load(f)
        prediction = model.predict(client_data)
        print(prediction)
    # call the writeToDB with the object
        writeToDB(predObj, prediction)
    #return 1:0
        return prediction


# Parse the object from the req, return the data
# TODO convert to numeric values
def parse_object(predObj):
    client_data = {
            'SeniorCitizen': predObj.get('SeniorCitizen'),
            'Partner': predObj.get('Partner'),
            'Dependents': predObj.get('Dependents'),
            'tenure': predObj.get('tenure'),
            'OnlineSecurity': predObj.get('OnlineSecurity'),
            'TechSupport': predObj.get('TechSupport'),
            'PaperlessBilling': predObj.get('PaperlessBilling'),
            'MonthlyCharges': predObj.get('MonthlyCharges'),
            'TotalCharges': predObj.get('TotalCharges'),
            'InternetService_DSL': predObj.get('InternetService_DSL'),
            'InternetService_Fiber_optic': predObj.get('InternetService_Fiber_optic'),
            'PaymentMethod_Credit_card': predObj.get('PaymentMethod_Credit_card'),
            'PaymentMethod_Electronic_check': predObj.get('PaymentMethod_Electronic_check'),
            'PaymentMethod_Mailed_check': predObj.get('PaymentMethod_Mailed_check'),
            'Contract_Month_to_month': predObj.get('Contract_Month-to-month'),
            'Contract_One_year': predObj.get('Contract_One_year'),
            'Contract_Two_year': predObj.get('Contract_Two_year'),
        }
    return client_data





if __name__ == '__main__':
    app.run(debug=True, port=5005)
