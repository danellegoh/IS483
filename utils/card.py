from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/healthpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Card(db.Model):
    __tablename__ = 'cards'
    
    card_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    collection_id = db.Column(db.Integer, nullable=False)
    points_required = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    recommendation = db.Column(db.String(300), nullable=False)

    def __init__(self, collection_id, title, points_required, description, recommendation, event_id=None):
        self.collection_id = collection_id
        self.title = title
        self.points_required = points_required
        self.event_id = event_id
        self.description = description
        self.recommendation = recommendation

    def json(self):
        return {
            "card_id": self.card_id,
            "collection_id": self.collection_id,
            "title": self.title,
            "points_required": self.points_required,
            "event_id": self.event_id,
            "description": self.description,
            "recommendation": self.recommendation
        }

# Create a new Card
@app.route('/card', methods=['POST'])
def create_card():
    data = request.json
    new_card = Card(
        collection_id=data.get('collection_id'),
        title=data.get('title'),
        points_required=data.get('points_required'),
        event_id=data.get('event_id'),
        description=data.get('description'),
        recommendation=data.get('recommendation')
    )
    try:
        db.session.add(new_card)
        db.session.commit()
        return jsonify(new_card.json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all Cards
@app.route('/cards', methods=['GET'])
def get_cards():
    cards = Card.query.all()
    return jsonify([card.json() for card in cards]), 200

# Get all Cards grouped by title
@app.route('/cards/grouped', methods=['GET'])
def get_cards_grouped():
    try:
        cards = Card.query.all()
        grouped_cards = defaultdict(list)

        for card in cards:
            grouped_cards[card.title].append(card.json())
        
        return jsonify({"code": 200, "data": grouped_cards}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all Cards by Collection ID
@app.route('/cards/collection/<int:collection_id>', methods=['GET'])
def get_cards_by_collection_id(collection_id):
    cards = Card.query.filter_by(collection_id=collection_id).all()
    if cards:
        return jsonify({"code": 200, "data": [card.json() for card in cards]}), 200
    return jsonify({"error": "No cards found for this collection_id"}), 404

# Get a Card by ID
@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    card = Card.query.get(card_id)
    if card:
        return jsonify({"code": 200, "data": card.json()}), 200
    return jsonify({"error": "Card not found"}), 404

# Update a Card by ID
@app.route('/card/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    card = Card.query.get(card_id)
    if card:
        data = request.json
        card.collection_id = data.get('collection_id', card.collection_id)
        card.title = data.get('title', card.title)
        card.points_required = data.get('points_required', card.points_required)
        card.event_id = data.get('event_id', card.event_id)
        card.description = data.get('description', card.description)
        card.recommendation = data.get('recommendation', card.recommendation)
        
        try:
            db.session.commit()
            return jsonify(card.json()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Card not found"}), 404

# Delete a Card by ID
@app.route('/card/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get(card_id)
    if card:
        try:
            db.session.delete(card)
            db.session.commit()
            return jsonify({"message": "Card deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Card not found"}), 404

if __name__ == '__main__':
    app.run(port=5003, debug=True)
