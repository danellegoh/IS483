import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Collection model
class Collection(db.Model):
    __tablename__ = 'collection'
    
    collection_id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(64), nullable=False)
    expired = db.Column(db.DateTime, nullable=True, default=True)

    def __init__(self, collection_name, expired=True):
        self.collection_name = collection_name
        self.expired = expired

    def json(self):
        return {
            "collection_id": self.collection_id,
            "collection_name": self.collection_name,
            "expired": self.expired
        }

# Create a new Collection
@app.route('/collection', methods=['POST'])
def create_collection():
    data = request.json
    new_collection = Collection(
        collection_name=data.get('collection_name'),
        expired=data.get('expired', True)  # Defaults to True if not specified
    )
    try:
        db.session.add(new_collection)
        db.session.commit()
        return jsonify(new_collection.json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all Collections
@app.route('/collections', methods=['GET'])
def get_collections():
    collections = Collection.query.all()
    return jsonify({ "code": 200, "data": [collection.json() for collection in collections]}), 200

# Get a Collection by ID
@app.route('/collection/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    collection = Collection.query.get(collection_id)
    if collection:
        return jsonify({"code": 200, "data": collection.json()}), 200
    return jsonify({"error": "Collection not found"}), 404

'''
Example of a successful GET API call
{
    "code": 200,
    "data": {
        "collection_id": 1,
        "collection_name": "Fruit Basket",
        "expired": true
    }
}
'''

# Update a Collection by ID
@app.route('/collection/<int:collection_id>', methods=['PUT'])
def update_collection(collection_id):
    collection = Collection.query.get(collection_id)
    if collection:
        data = request.json
        collection.collection_name = data.get('collection_name', collection.collection_name)
        collection.expired = data.get('expired', collection.expired)
        
        try:
            db.session.commit()
            return jsonify(collection.json()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Collection not found"}), 404

# Partially update a Collection by ID
@app.route('/collection/<int:collection_id>', methods=['PATCH'])
def patch_collection(collection_id):
    collection = Collection.query.get(collection_id)
    if collection:
        data = request.json
        if 'collection_name' in data:
            collection.collection_name = data['collection_name']
        if 'expired' in data:
            collection.expired = data['expired']
        
        try:
            db.session.commit()
            return jsonify(collection.json()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Collection not found"}), 404

# Delete a Collection by ID
@app.route('/collection/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    collection = Collection.query.get(collection_id)
    if collection:
        try:
            db.session.delete(collection)
            db.session.commit()
            return jsonify({"message": "Collection deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Collection not found"}), 404

# if __name__ == '__main__':
#     app.run(port=5022, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')