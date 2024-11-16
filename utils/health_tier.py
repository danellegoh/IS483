from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import pickle
import numpy as np
from datetime import datetime
import pandas as pd
import sklearn
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URI')
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

# Load the model and create the tier mapping
with open('health_tier_cluster_model.pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

# Sort clusters by centers and map to tiers
sorted_clusters = sorted(
    enumerate(kmeans.cluster_centers_), 
    key=lambda x: (x[1][0], x[1][1]) 
)
cluster_to_tier = {cluster_idx: tier + 1 for tier, (cluster_idx, _) in enumerate(sorted_clusters)}

def predict_health_tier(user_data):
    try:
        # Ensure user_data has required fields
        required_fields = ['preferred_intensity', 'target_minutes']
        missing_fields = [field for field in required_fields if field not in user_data]

        if missing_fields:
            raise ValueError(f"Input data is missing fields: {', '.join(missing_fields)}")

        # Convert user_data to DataFrame and predict
        filtered_data_df = pd.DataFrame([user_data], columns=required_fields)
        cluster = kmeans.predict(filtered_data_df)[0]
        
        # Map cluster to health tier
        return cluster_to_tier.get(cluster, None)

    except ValueError as ve:
        print(f"Input error: {str(ve)}")
        return None
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None

    
# Update partial fields of user by user ID
@app.route('/user/tier/id/<int:user_id>', methods=['PATCH'])
def partial_update_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json

        # Update fields only if they are provided in the request
        if 'name' in data:
            user.name = data['name']
        if 'birthdate' in data:
            user.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
        if 'gender' in data:
            user.gender = data['gender']
        if 'height' in data:
            user.height = data['height']
        if 'weight' in data:
            user.weight = data['weight']
        if 'contact_details' in data:
            user.contact_details = data['contact_details']
        if 'nationality' in data:
            user.nationality = data['nationality']
        if 'location_group' in data:
            user.location_group = data['location_group']
        if 'school' in data:
            user.school = data['school']
        if 'password' in data:
            user.password = data['password']
        if 'role' in data:
            user.role = data['role']
        if 'last_login' in data:
            user.last_login = datetime.strptime(data['last_login'], '%Y-%m-%d %H:%M:%S')
        if 'total_point' in data:
            user.total_point = data['total_point']
        if 'goal_date' in data:
            user.goal_date = datetime.strptime(data['goal_date'], '%Y-%m-%d')

        try:
            # Update target_minutes and preferred_intensity if provided
            if 'target_minutes' in data:
                user.target_minutes = data['target_minutes']
            if 'preferred_intensity' in data:
                user.preferred_intensity = data['preferred_intensity']

            # Prepare user data for prediction as a dictionary
            user_data = {
                'preferred_intensity': user.preferred_intensity,
                'target_minutes': user.target_minutes
            }

            # Predict the new health tier and apply it
            predicted_tier = predict_health_tier(user_data)
            print(f"Predicted health tier for user {user_id}: {predicted_tier}")  # Debugging line

            if predicted_tier is not None:
                user.health_tier = predicted_tier
            else:
                return jsonify({"error": "Failed to predict health tier"}), 500

            db.session.commit()
            return jsonify({"code": 200, "data": user.json()}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "User not found"}), 404

    
@app.route('/test_kmeans', methods=['GET'])
def test_kmeans():
    # Check if kmeans model is loaded and return its type
    model_type = type(kmeans).__name__
    return jsonify({"model_type": model_type}), 200

@app.route('/test_kmeans_prediction', methods=['GET'])
def test_kmeans_prediction():
    # Sample input data to test if kmeans model works
    test_data = {
        "preferred_intensity": 4,
        "target_minutes": 250
    }
    
    try:
        # Test prediction on sample data
        cluster = predict_health_tier(test_data)
        return jsonify({"status": "success", "predicted_cluster": cluster}), 200
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5041, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')