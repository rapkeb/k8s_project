from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db = client['churn_prediction']  # Replace with your database name
collection = db['raw_data']  # Replace with your collection name


@app.route('/submit/<user_id>', methods=['GET'])
def submit(user_id):
    # Query MongoDB for the specific user
    user = collection.find_one({"customerID": user_id})

    if user:
        user.pop('_id')  # Remove MongoDB's internal ID field if needed
        return jsonify(user)
    else:
        return jsonify({"error": f"User ID {user_id} not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5005)
