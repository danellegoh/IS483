from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
from os import environ
import hashlib

app = Flask(__name__)
CORS(app)

VERCEL_BASE_URL = os.getenv('VERCEL_BASE_URL')

# user_URL = "http://localhost:5001/user"
user_URL = f"{VERCEL_BASE_URL}/user"

@app.route("/user_login", methods=['POST'])
def user_login():
    if request.is_json:
        try:
            login_information = request.get_json()
            print("\nReceived login information in JSON:", login_information)
            result = processLoginInformation(login_information)
            return jsonify(result), result['code']
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            
            return jsonify({
                "code": 500,
                "message": "user_login.py internal error: " + ex_str
            }), 500

def processLoginInformation(login_information):
    
    # 1. Extract email and password from login information
    email = login_information['email']
    password = login_information['password']
    
    if not email or not password:
        return {
            "code": 400,
            "message": "Missing email or password"
        }
    
    # 2. Check if user exists by email
    print('\n-----Invoking user microservice for login-----')
    user_result = invoke_http(f"{user_URL}/{email}", method='GET')
    print('user_result:', user_result)
    
    user_result_code = user_result["code"]
    
    # 4. If user is found, verify the password
    if user_result_code == 200:
        user_data = user_result["data"]
        stored_password = user_data['password']
        
        if stored_password == password:
            
            # No fail condition to update today's datetime
            user_result = invoke_http(f"{user_URL}/{email}", method='PUT')
            print(user_result)
            return {
                "code": 200,
                "message": "Login successful",
                "data": {
                    "user_id": user_data,
                    "name": user_data,
                    "email": user_data,
                    "role": user_data,
                    "last_login": user_data
                }
            }
        else:
            return {
                "code": 404,
                "message": "Invalid password"
            }
    
    # 5. If user not found, return error
    elif user_result_code == 404:
        return {
            "code": 404,
            "message": "User not found"
        }
    
    # 6. Handle unexpected error codes
    else:
        return {
            "code": user_result_code,
            "message": "An error occurred while logging in",
            "data": {"user_result": user_result["data"]}
        }

# if __name__ == "__main__":
#     app.run(port=5009, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
