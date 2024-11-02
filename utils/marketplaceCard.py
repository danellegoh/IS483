from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
from os import environ
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)

collection_URL = "http://localhost:5022/collection"
card_URL = "http://localhost:5003/card"

@app.route("/available_cards", methods=['GET'])
def trade_card():
    if request.is_json:
        try:
            result = processAvailableCards()
            return jsonify(result), result['code']
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            
            return jsonify({
                "code": 500,
                "message": "trade_card.py internal error: " + ex_str
            }), 500
            
def processAvailableCards():

    collection_result = invoke_http(f"{collection_URL}s", method='GET')
    '''
    Example of collection_result 
    - Returns all collection information 
    {
        "code": 200,
        "data": [
            {
                "collection_id": 1,
                "collection_name": "Fruit Basket",
                "expired": true
            },
            {
                "collection_id": 2,
                "collection_name": "Weekend Action",
                "expired": false
            }
        ]
    }
    '''
    
    available_collections = []
    if collection_result['code'] == 200:
        try:
            for collection in collection_result['data']:
                # Checks if collection should be available for purchase (Limited Edition)
                if collection["expired"] == True:
                    available_collections.append(collection["collection_id"])
        except:
            print("No available collection")
        
    else:
        print("failed get collections")
    
    available_cards = []
    for collection_id in available_collections:
        # If collection can be purchased, we will get all the cards in it to display in the marketplace
        card_result = invoke_http(f"{card_URL}s/collection/{collection_id}", method='GET')
        
        '''
        Example of card_result
        - Returns all cards that are available for purchase
        {
            "code": 200,
            "data": [
                {
                    "card_id": 1,
                    "collection_id": 1,
                    "description": "Oranges are actually a type of berry! They’re one of the most popular fruits in the world.",
                    "event_id": 1,
                    "points_required": 500,
                    "recommendation": "1-2 oranges per day provides a good dose of vitamin C, which boosts your immune system.",
                    "title": "Oliver"
                },
                {
                    "card_id": 2,
                    "collection_id": 1,
                    "description": "Strawberries aren't true berries by botanical definition, they are part of the rose family.",
                    "event_id": null,
                    "points_required": 500,
                    "recommendation": "The daily fruit intake recommendation is 1.5-2cups of fruit per day. Munch on 12-16 strawberries as part of your healthy diet with this rich source of vitamin C, fibre and antioxident",
                    "title": "Selena"
                },
                {
                    "card_id": 3,
                    "collection_id": 1,
                    "description": "Pineapple is not a single fruit, but a cluster of hundreds of tiny fruitlets fused together!",
                    "event_id": null,
                    "points_required": 500,
                    "recommendation": "Eating 1-2 slices a day aids digestion and provides a good dose of vitamin C and manganese.",
                    "title": "Penny"
                },
                {
                    "card_id": 4,
                    "collection_id": 1,
                    "description": "There are over 8,000 varieties of grapes around the world! Some types have been around for over 6,000 years.",
                    "event_id": null,
                    "points_required": 500,
                    "recommendation": "A small bunch (about 1 cup) of grapes is a refreshing, heart-healthy snack full of antioxidants.",
                    "title": "Gracia"
                },
                {
                    "card_id": 5,
                    "collection_id": 1,
                    "description": "Bananas are technically berries too, and they can float in water!",
                    "event_id": null,
                    "points_required": 500,
                    "recommendation": "1-2 bananas a day helps provide potassium for muscle function and maintaining healthy blood pressure.",
                    "title": "Benny"
                }
            ]
        }
    '''
    
        if card_result['code'] == 200: 
            available_cards= available_cards+card_result["data"]
        
        else:
            collection_name = collection["collection_name"]
            print(f"failed to get cards from {collection_name}")
    
    return {"code": 200, "data": available_cards}

    '''
    To be Returned
    {
        "code": 200,
        "data": [
            {
                "card_id": 1,
                "collection_id": 1,
                "description": "Oranges are actually a type of berry! They’re one of the most popular fruits in the world.",
                "event_id": 1,
                "points_required": 500,
                "recommendation": "1-2 oranges per day provides a good dose of vitamin C, which boosts your immune system.",
                "title": "Oliver"
            },
            {
                "card_id": 2,
                "collection_id": 1,
                "description": "Strawberries aren't true berries by botanical definition, they are part of the rose family.",
                "event_id": null,
                "points_required": 500,
                "recommendation": "The daily fruit intake recommendation is 1.5-2cups of fruit per day. Munch on 12-16 strawberries as part of your healthy diet with this rich source of vitamin C, fibre and antioxident",
                "title": "Selena"
            },
            {
                "card_id": 3,
                "collection_id": 1,
                "description": "Pineapple is not a single fruit, but a cluster of hundreds of tiny fruitlets fused together!",
                "event_id": null,
                "points_required": 500,
                "recommendation": "Eating 1-2 slices a day aids digestion and provides a good dose of vitamin C and manganese.",
                "title": "Penny"
            },
            {
                "card_id": 4,
                "collection_id": 1,
                "description": "There are over 8,000 varieties of grapes around the world! Some types have been around for over 6,000 years.",
                "event_id": null,
                "points_required": 500,
                "recommendation": "A small bunch (about 1 cup) of grapes is a refreshing, heart-healthy snack full of antioxidants.",
                "title": "Gracia"
            },
            {
                "card_id": 5,
                "collection_id": 1,
                "description": "Bananas are technically berries too, and they can float in water!",
                "event_id": null,
                "points_required": 500,
                "recommendation": "1-2 bananas a day helps provide potassium for muscle function and maintaining healthy blood pressure.",
                "title": "Benny"
            }
        ]
    }
'''
        
if __name__ == '__main__':
    app.run(port=5023, debug=True)