from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from invokes import invoke_http

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

userURL = "http://localhost:5001/user"
cardURL = "http://localhost:5003/card"

class Trade(db.Model):
    __tablename__ = 'trade'
    
    trade_id = db.Column(db.Integer, primary_key=True)
    
    # Trader One
    # user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # card_one_id = db.Column(db.Integer, db.ForeignKey('card.card_id'), nullable=False)
    user_id = db.Column(db.Integer,  nullable=False)
    card_one_id = db.Column(db.Integer,  nullable=False)
    # card_one_name = db.Column(db.String(255), nullable=False)
    card_earned_date = db.Column(db.DateTime, nullable=False)
    
    # Trader Two
    # trader_two_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    card_two_id = db.Column(db.Integer,  nullable=True)
    # card_two_name = db.Column(db.String(255), nullable=True)
    # two_earned_date = db.Column(db.DateTime, nullable=True)
    
    # traded = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, card_one_id, card_earned_date, card_two_id):
        self.user_id = user_id
        self.card_one_id = card_one_id
        # self.card_one_name = card_one_name
        self.card_earned_date = card_earned_date
        # self.trader_two_id = trader_two_id
        self.card_two_id = card_two_id
        # self.card_two_name = card_two_name
        # self.two_earned_date = two_earned_date
        # self.traded = traded

    def json(self):
        return {
            "trade_id": self.trade_id,
            "user_id": self.user_id,
            "card_one_id": self.card_one_id,
            # "card_one_name": self.card_one_name,
            "card_earned_date": self.card_earned_date.isoformat(),
            # "trader_two_id": self.trader_two_id,
            "card_two_id": self.card_two_id,
            # "card_two_name": self.card_two_name,
            # "two_earned_date": self.two_earned_date.isoformat(),
            # "traded": self.traded
        }

# Create a new Trade
@app.route('/trade', methods=['POST'])
def create_trade():
    data = request.json
    new_trade = Trade(
        user_id=data.get('user_id'),
        card_one_id=data.get('card_one_id'),
        # card_one_name=data.get('card_one_name'),
        card_earned_date=datetime.strptime(data.get('card_earned_date'), '%Y-%m-%dT%H:%M:%S'),
        # trader_two_id=data.get('trader_two_id'),
        card_two_id=data.get('card_two_id'),
        # card_two_name=data.get('card_two_name'),
        # two_earned_date=datetime.strptime(data.get('two_earned_date'), '%Y-%m-%dT%H:%M:%S'),
        # traded=data.get('traded', False)
    )
    
    try:
        db.session.add(new_trade)
        db.session.commit()
        return jsonify(new_trade.json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all Trades
@app.route('/trades', methods=['GET'])
def get_trades():
    try:
        trades = Trade.query.all()
        output = []
        for trade in trades:
            trade_id = trade.trade_id
            user_id = trade.user_id
            card_one_id = trade.card_one_id
            card_two_id = trade.card_two_id

            user_response = invoke_http(userURL+f"/id/{user_id}")
            card_one_response = invoke_http(cardURL+f"/{card_one_id}")
            card_two_response = invoke_http(cardURL+f"/{card_two_id}")
            # print(user_response)
            # print(card_one_response)
            # print(card_two_response)

            if user_response["code"] == 200 and card_one_response["code"] == 200 and card_two_response["code"] == 200:
                # print("check 1")
                name = user_response["data"]["name"]
                card_one_title = card_one_response["data"]["title"]
                card_one_type = card_one_response["data"]["card_type"]
                card_two_title = card_two_response["data"]["title"]
                card_one_type = card_two_response["data"]["card_type"]
                output.append({"trade_id": trade_id, "user_id": user_id, "name": name, 
                            "card_one_id": card_one_id, "card_one_title": card_one_title, "card_one_type": card_one_type, 
                            "card_two_id": card_two_id, "card_two_title": card_two_title, "card_two_type": card_one_type})

        return jsonify({"code": 200, "data": output}), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

# Get a Trade by ID
@app.route('/trade/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    trade = Trade.query.get(trade_id)
    if trade:
        return jsonify(trade.json()), 200
    return jsonify({"error": "Trade not found"}), 404

# Update a Trade by ID
# @app.route('/trade/<int:trade_id>', methods=['PUT'])
# def update_trade(trade_id):
#     trade = Trade.query.get(trade_id)
#     if trade:
#         data = request.json
#         trade.user_id = data.get('user_id', trade.user_id)
#         trade.card_one_id = data.get('card_one_id', trade.card_one_id)
#         trade.card_one_name = data.get('card_one_name', trade.card_one_name)
#         trade.card_earned_date = datetime.strptime(data.get('card_earned_date'), '%Y-%m-%dT%H:%M:%S') if data.get('card_earned_date') else trade.card_earned_date
#         trade.trader_two_id = data.get('trader_two_id', trade.trader_two_id)
#         trade.card_two_id = data.get('card_two_id', trade.card_two_id)
#         trade.card_two_name = data.get('card_two_name', trade.card_two_name)
#         trade.two_earned_date = datetime.strptime(data.get('two_earned_date'), '%Y-%m-%dT%H:%M:%S') if data.get('two_earned_date') else trade.two_earned_date
#         trade.traded = data.get('traded', trade.traded)
        
#         try:
#             db.session.commit()
#             return jsonify(trade.json()), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": str(e)}), 400
#     return jsonify({"error": "Trade not found"}), 404

# Delete a Trade by ID
@app.route('/trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    trade = Trade.query.get(trade_id)
    if trade:
        try:
            db.session.delete(trade)
            db.session.commit()
            return jsonify({"code": 200, "message": "Trade deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 400, "error": str(e)}), 400
    return jsonify({"code": 404, "error": "Trade not found"}), 404

if __name__ == '__main__':
    app.run(port=5010, debug=True)

