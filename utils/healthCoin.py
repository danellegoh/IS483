import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from .user import User
from flask_cors import CORS, cross_origin

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)
CORS(app)

class HealthCoins(db.Model):
    __tablename__ = 'health_coin'
    
    points_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    points_earned = db.Column(db.Integer, nullable=False)
    earned_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    source = db.Column(db.String(64), nullable=False)

    def __init__(self, points_id, user_id, points_earned, source, earned_date=None):
        self.points_id = points_id
        self.user_id = user_id
        self.points_earned = points_earned
        self.earned_date = datetime.now()
        self.source = source

    def json(self):
        return {
            "points_id": self.points_id,
            "user_id": self.user_id,
            "points_earned": self.points_earned,
            "earned_date": self.earned_date.isoformat(),
            "source": self.source
        }

# Get the next points_id
def get_next_points_id():
    try:
        # Get the maximum points_id from the table
        max_points_id = db.session.query(db.func.max(HealthCoins.points_id)).scalar()
        # If there are no UserCards yet, start with points_id 1
        if max_points_id is None:
            return 1
        return max_points_id + 1
    except Exception as e:
        print(f"Error getting next points_id: {str(e)}")
        return None
    
# Create a new HealthCoins entry
@app.route('/healthcoins', methods=['POST'])
def create_health_coins():
    data = request.json
    next_points_id = get_next_points_id()

    if next_points_id is None:
        return jsonify({"error": "Unable to generate points_id"}), 400

    new_health_coins = HealthCoins(
        points_id=next_points_id,
        user_id=data.get('user_id'),
        points_earned=data.get('points_earned'),
        earned_date=data.get('earned_date'),
        source=data.get('source')
    )
    try:
        db.session.add(new_health_coins)
        db.session.commit()
        return jsonify({"code": 201, "data": new_health_coins.json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all HealthCoins entries
@app.route('/healthcoins', methods=['GET'])
def get_health_coins():
    health_coins_list = HealthCoins.query.all()
    return jsonify([hc.json() for hc in health_coins_list]), 200

# Get a HealthCoins entry by ID
@app.route('/healthcoins/<int:points_id>', methods=['GET'])
def get_health_coins_by_id(points_id):
    health_coins = HealthCoins.query.get(points_id)
    if health_coins:
        return jsonify(health_coins.json()), 200
    return jsonify({"error": "HealthCoins entry not found"}), 404

# Update a HealthCoins entry by ID
@app.route('/healthcoins/<int:points_id>', methods=['PUT'])
def update_health_coins(points_id):
    health_coins = HealthCoins.query.get(points_id)
    if health_coins:
        data = request.json
        health_coins.user_id = data.get('user_id', health_coins.user_id)
        health_coins.points_earned = data.get('points_earned', health_coins.points_earned)
        health_coins.earned_date = data.get('earned_date', health_coins.earned_date)
        health_coins.source = data.get('source', health_coins.source)
        
        try:
            db.session.commit()
            return jsonify(health_coins.json()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "HealthCoins entry not found"}), 404

# Delete a HealthCoins entry by ID
@app.route('/healthcoins/<int:points_id>', methods=['DELETE'])
def delete_health_coins(points_id):
    health_coins = HealthCoins.query.get(points_id)
    if health_coins:
        try:
            db.session.delete(health_coins)
            db.session.commit()
            return jsonify({"message": "HealthCoins entry deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "HealthCoins entry not found"}), 404

# if __name__ == '__main__':
#     app.run(port=5004, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')