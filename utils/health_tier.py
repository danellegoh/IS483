from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import pickle
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans
import pandas as pd
import sklearn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    gender = db.Column(db.String(64), nullable = False)
    height = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    contact_details = db.Column(db.String(64), nullable = False)
    nationality = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(64), nullable = False, unique = True)
    location_group = db.Column(db.String(64), nullable = False)
    school = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(64), nullable = False) 
    parent_id = db.Column(db.String(64), db.ForeignKey('user.user_id'), nullable = True) 
    role = db.Column(db.String(64), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False)
    last_login = db.Column(db.DateTime, nullable = False)
    total_point = db.Column(db.Integer, nullable = False)
    health_tier = db.Column(db.Integer, nullable = False)
    # children = db.relationship('User', backref = db.backref('parent', remote_side =[user_id]), lazy = True)
    target_minutes = db.Column(db.Integer, nullable = False)
    preferred_intensity = db.Column(db.Integer, nullable = False)
    goal_date = db.Column(db.Date, nullable = False)
    
    def __init__(self, user_id, name, birthdate, gender, height, weight, contact_details, nationality, email, location_group, school, password, target_minutes, preferred_intensity, goal_date, parent_id=None, role='User', created_date=None, last_login=None, total_point=0, health_tier = 0):
        self.user_id = user_id
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.height = height
        self.weight = weight
        self.contact_details = contact_details
        self.nationality = nationality
        self.email = email
        self.location_group = location_group
        self.school = school
        self.password = password
        self.parent_id = parent_id
        self.role = role
        self.created_date = datetime.now()
        self.last_login = datetime.now()
        self.total_point = 0
        self.health_tier = 1 
        self.target_minutes = target_minutes
        self.preferred_intensity = preferred_intensity
        self.goal_date = goal_date

    def json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "birthdate": self.birthdate.isoformat(),
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "contact_details": self.contact_details,
            "nationality": self.nationality,
            "email": self.email,
            "location_group": self.location_group,
            "school": self.school,
            "password": self.password,
            "parent_id": self.parent_id,
            "role": self.role,
            "created_date": self.created_date.isoformat(),
            "last_login": self.last_login.isoformat(),
            "total_point": self.total_point,
            "health_tier":self.health_tier,
            "target_minutes": self.target_minutes,
            "preferred_intensity": self.preferred_intensity,
            "goal_date": self.goal_date.isoformat()
        }
        
# Load the model
file_path = 'health_tier_cluster_model.pkl'
kmeans_model = None
cluster_to_tier = None

def load_model():
    global kmeans_model, cluster_to_tier
    try:
        with open(file_path, 'rb') as file:
            kmeans_model = pickle.load(file)
        print("Model loaded successfully.")
        
        # Map clusters to tiers based on target_minutes
        cluster_centers = kmeans_model.cluster_centers_
        sorted_clusters = sorted(enumerate(cluster_centers), key=lambda x: x[1][1])  # Sort by 'target_minutes'
        cluster_to_tier = {cluster_idx: tier + 1 for tier, (cluster_idx, _) in enumerate(sorted_clusters)}
    except Exception as e:
        print(f"An error occurred while loading the pickle file: {e}")

# Load the model once when starting the server
load_model()

# Function to predict the tier for given user data
def predict_tier(target_minutes=None, preferred_intensity=None):
    try:
        # Use sample data for testing if inputs are None
        if target_minutes is None and preferred_intensity is None:
            target_minutes = 250
            preferred_intensity = 4
            print("Using sample data for testing: target_minutes=250, preferred_intensity=4")

        # Construct input DataFrame in the required feature order
        input_data = pd.DataFrame({
            'preferred_intensity': [preferred_intensity],
            'target_minutes': [target_minutes]
        })

        # Print input data for debugging
        print("Input data for prediction:", input_data)

        # Ensure model is loaded and ready
        if kmeans_model is None:
            print("Error: kmeans_model is not loaded.")
            return None

        # Print model details for debugging
        print("Model cluster centers:", kmeans_model.cluster_centers_)
        if hasattr(kmeans_model, 'feature_names_in_'):
            print("Expected feature names:", kmeans_model.feature_names_in_)
        else:
            print("No feature names attribute in the model.")

        # Perform the prediction
        predicted_cluster = kmeans_model.predict(input_data)[0]

        # Map the predicted cluster to a tier
        predicted_tier = cluster_to_tier.get(predicted_cluster)
        print("Predicted cluster:", predicted_cluster)
        print("Mapped tier:", predicted_tier)

        return predicted_tier
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

# Check model loading
@app.route('/check_model', methods=['GET'])
def check_model():
    if kmeans_model is not None and cluster_to_tier is not None:
        sample_data = {
            "cluster_centers": kmeans_model.cluster_centers_.tolist(),
            "cluster_to_tier_mapping": cluster_to_tier
        }
        return jsonify({"message": "Model loaded successfully.", "sample_data": sample_data}), 200
    else:
        return jsonify({"error": "Model not loaded."}), 500

# Predict tier for user data
@app.route('/predict_tier', methods=['POST'])
def predict():
    data = request.get_json()
    target_minutes = data.get("target_minutes")
    preferred_intensity = data.get("preferred_intensity")
    
    if target_minutes is None or preferred_intensity is None:
        return jsonify({"error": "Please provide 'target_minutes' and 'preferred_intensity'"}), 400

    predicted_tier = predict_tier(target_minutes, preferred_intensity)
    if predicted_tier is None:
        return jsonify({"error": "Prediction failed."}), 500
    
    return jsonify({"predicted_tier": predicted_tier})

# Update partial fields of user by email
@app.route('/user/<string:email>', methods=['PATCH'])
def partial_update_user(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
        if key == "birthdate" or key == "goal_date":
            setattr(user, key, datetime.strptime(value, '%Y-%m-%d'))

    # Update target_minutes and preferred_intensity, and predict health tier if needed
    if "target_minutes" in data or "preferred_intensity" in data:
        target_minutes = data.get("target_minutes", user.target_minutes)
        preferred_intensity = data.get("preferred_intensity", user.preferred_intensity)
        predicted_tier = predict_tier(target_minutes, preferred_intensity)
        if predicted_tier is not None:
            user.health_tier = predicted_tier
        else:
            return jsonify({"error": "Failed to predict health tier"}), 500

    db.session.commit()
    return jsonify({"code": 200, "data": user.json()}), 200

@app.route('/get_feature_names', methods=['GET'])
def get_feature_names():
    if hasattr(kmeans_model, 'feature_names_in_'):
        # Return the feature names if available
        return jsonify({"feature_names": kmeans_model.feature_names_in_.tolist()}), 200
    else:
        # Inform that feature names are not available in the model
        return jsonify({"error": "Feature names not available in the model."}), 404


if __name__ == '__main__':
    app.run(port=5041, debug=True)