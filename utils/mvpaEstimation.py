from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
from os import environ
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)
CORS(app)

VERCEL_BASE_URL = os.getenv('VERCEL_BASE_URL')

# strava_URL = "http://localhost:5020"
strava_URL = f"{VERCEL_BASE_URL}/activities"

class strava_users(db.Model):
    tablename = 'strava_users'
    
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.String(50), unique=True, nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    refresh_token = db.Column(db.String(200), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

    def __init__(self, id, strava_id, access_token, refresh_token, expires_at):
        self.id = id
        self.strava_id = strava_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def json(self):
        return {
            "id": self.id,
            "strava_id": self.strava_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at
        }

@app.route('/check_activities_access', methods=['GET'])
def check_activities_access():
    try:
        # Step 1: Fetch user data from the database (assuming first user for now)
        user = strava_users.query.first()

        if not user:
            return jsonify({"code": 404, "message": "User not found"}), 404

        # Step 3: Use invoke_http to fetch activities from Strava
        headers = {'Authorization': f'Bearer {user.access_token}'}
        # activities_response = invoke_http(f"{strava_URL}/activities", method="GET", headers=headers)
        activities_response = invoke_http(strava_URL, method="GET", headers=headers)

        # print(f'{strava_URL}/activities')
        print(strava_URL)

        # Step 4: Check if the response contains an error
        if activities_response.get('code', 200) != 200:
            raise Exception(f"Failed to fetch activities: {activities_response.get('message', 'Unknown error')}")

        # Step 5: If activities are fetched, return the activities data
        activities = activities_response.get("data")
        if activities:
            return jsonify({
                "code": 200,
                "message": "Successfully accessed activities data",
                "data": activities
            }), 200
        else:
            return jsonify({
                "code": 204,
                "message": "No activities found"
            }), 204

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "Internal error: " + ex_str
        }), 500


# Calculate weekly MVPA based on speed of activities
@app.route('/estimate_mvpa', methods=['GET'])
def estimate_mvpa():
    try:
        # Step 1: Fetch user data from the database
        user = strava_users.query.first()  # Adjust this query as necessary

        if not user:
            return jsonify({"code": 404, "message": "User not found"}), 404

        # Step 2: Call the Strava API to get activities
        result = processStravaInformation(user.access_token)
        return jsonify(result)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "Internal error: " + ex_str
        }), 500

def processStravaInformation(access_token):
    # Set up authorization headers
    headers = {'Authorization': f'Bearer {access_token}'}

    # Step 1: Fetch activities from Strava API
    # activities_response = invoke_http(f'{strava_URL}/activities', method='GET', headers=headers)
    activities_response = invoke_http(strava_URL, method='GET', headers=headers)

    activities = activities_response.get("data")

    # Initialize variables for tracking weekly stats
    current_week = datetime.now().isocalendar()[1]
    weekly_distance = 0
    weekly_time = 0
    
    daily_met = 0
    to_return = {
        "weekly_met": 0,
        "weekly_time_lapse": 0,
        "daily_time_lapse": 0,
        "monthly_time_lapse": 0,
        "monthly_top_activity": "",
        "activities_in_month": {}, # key: date, value: distance
        "monthly_distance": 0
    }

    weekly_time_lapse = 0
    monthly_time_lapse = 0
    monthly_distance = 0
    activity_dict = {}

    ### monthly report
    now = datetime.now()
    if now.month == 1:
        last_month = 12
    else:
        last_month = now.month - 1

    # process activity data
    for activity in activities:
        activity_date = datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
        
        if activity_date.month == datetime.now().month: # check for current month
            if activity_date.isocalendar()[1] == current_week: # check week

                weekly_distance += activity.get("distance", 0)
                weekly_time += activity.get("elapsed_time", 0)

                if activity_date.date() == datetime.now().date(): # today in current week
                    speed_m_s = activity.get("distance", 0) / activity.get("elapsed_time", 1)
                    daily_met = (speed_m_s / 0.2) + 3.5
                    if daily_met >= 3:
                        to_return["daily_time_lapse"] = round(activity.get("elapsed_time", 0) / 60, 0)
                        weekly_time_lapse += round(activity.get("elapsed_time", 0) / 60, 0)
                
                else: # other days in current week
                    speed_m_s = activity.get("distance", 0)
                    daily_met = (speed_m_s / 0.2) + 3.5
                    if daily_met >= 3:
                        weekly_time_lapse += round(activity.get("elapsed_time", 0) / 60, 0)

        elif activity_date.month == last_month: # check for last month
            # total activity for last month
            speed_m_s = activity.get("distance", 0)
            daily_met = (speed_m_s / 0.2) + 3.5
            if daily_met >= 3:
                monthly_time_lapse += round(activity.get("elapsed_time", 0) / 60, 0)
            
            # top activity for last month
            sport_type = activity.get("sport_type")
            if sport_type not in activity_dict:
                activity_dict[sport_type] = 1
            else:
                activity_dict[sport_type] += 1
            
            # store activities for last month
            to_return["activities_in_month"][activity_date.day] = activity.get("distance", 0)
            monthly_distance += activity.get("distance", 0)

        else:
            break
    
    to_return["weekly_time_lapse"] = weekly_time_lapse
    to_return["monthly_time_lapse"] = monthly_time_lapse
    to_return["monthly_distance"] = monthly_distance

    if weekly_time > 0:
        weekly_speed_m_s = weekly_distance / weekly_time
        to_return["weekly_met"] = (weekly_speed_m_s / 0.2) + 3.5



    # Determine the top activity for the previous month            
    if activity_dict:
        top_activity = max(activity_dict, key=activity_dict.get)
        to_return["monthly_top_activity"] = top_activity


    return to_return

# if __name__ == '__main__':
#     app.run(port=5021, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')