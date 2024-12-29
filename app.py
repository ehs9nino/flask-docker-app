from flask import Flask, request, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Default to local MongoDB
client = MongoClient(MONGO_URI)
db = client["user_management"]
collection = db["users"]

@app.route("/")
def home():
    return "Welcome to the Flask MongoDB App!"

# Add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        existing_user = collection.find_one({"email": data["email"]})
        if existing_user:
            return jsonify({"error": "User already exists!"}), 400

        result = collection.insert_one(data)  # Insert the user data into MongoDB
        user = {"_id": str(result.inserted_id), **data}  # Convert ObjectId to string
        return jsonify({"message": "User added successfully!", "user": user}), 201
    except Exception as e:
        print(f"Error adding user: {e}")  # Log the error
        return jsonify({"error": "Internal Server Error"}), 500


# Get user information
@app.route("/get_user", methods=["GET"])
def get_user():
    email = request.args.get("email")
    
    if not email:
        return jsonify({"error": "Email is required!"}), 400

    user = collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found!"}), 404

    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return jsonify(user)

# Update user information
@app.route("/update_user", methods=["PUT"])
def update_user():
    data = request.json
    email = data.get("email")
    age = data.get("age")
    
    if not email or not age:
        return jsonify({"error": "Email and age are required!"}), 400

    result = collection.update_one({"email": email}, {"$set": {"age": age}})
    if result.matched_count == 0:
        return jsonify({"error": "User not found!"}), 404

    return jsonify({"message": "User updated successfully!"})

# Delete a user
@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    data = request.json
    email = data.get("email")
    
    if not email:
        return jsonify({"error": "Email is required!"}), 400

    result = collection.delete_one({"email": email})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found!"}), 404

    return jsonify({"message": "User deleted successfully!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    app.run(host="0.0.0.0", port=port)
