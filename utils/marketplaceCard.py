from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
from os import environ
import hashlib
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

VERCEL_BASE_URL = os.getenv('VERCEL_BASE_URL')

# collection_URL = "http://localhost:5022/collection"
# card_URL = "http://localhost:5003/card"
collection_URL = f"{VERCEL_BASE_URL}/collection"
card_URL = f"{VERCEL_BASE_URL}/card"

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
    
        if card_result['code'] == 200: 
            available_cards= available_cards+card_result["data"]
        
        else:
            collection_name = collection["collection_name"]
            print(f"failed to get cards from {collection_name}")
    
    return {"code": 200, "data": available_cards}
        
# if __name__ == '__main__':
#     app.run(port=5023, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')