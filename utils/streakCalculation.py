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

VERCEL_BASE_URL = os.getenv('VERCEL_BASE_URL')

# goal_URL = "http://localhost:5011/goal"
# streak_URL = "http://localhost:5010/streak"
# mvp_URL = "http://localhost:5021/estimate_mvpa"
# coin_URL = "http://localhost:5004/healthcoins"
# user_URL = "http://localhost:5001/user"
goal_URL = f"{VERCEL_BASE_URL}/goal"
streak_URL = f"{VERCEL_BASE_URL}/streak"
mvp_URL = f"{VERCEL_BASE_URL}/estimate_mvpa"
coin_URL = f"{VERCEL_BASE_URL}/healthcoins"
user_URL = f"{VERCEL_BASE_URL}/user"

@app.route('/update_streak', methods=['POST'])
def update_streak_if_mvpa():
    if request.is_json:
        try:
            streak_information = request.get_json()
            print("\nReceived streak information in JSON:", streak_information)
            result = processStreakInformation(streak_information)
            print(result)
            return jsonify(result[0]), result[1]
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            
            return jsonify({
                "code": 500,
                "message": "streakCalculation.py internal error: " + ex_str
            }), 500
    else: 
        print("wrong input")

def processStreakInformation(streak_information):
    try:
        goal_id = streak_information['goal_id']
        user_id = streak_information['user_id']
        streak_id = streak_information['streak_id']
        
        # Get Goal of User by Goal ID
        goal_result = invoke_http(f"{goal_URL}/{goal_id}", method='GET')
        print("goal", goal_result)
        
        # Get Estimated MET
        met_result = invoke_http(f"{mvp_URL}")
        print("mvpaEstimation", met_result)
        estimated_met = met_result["weekly_met"]
        
        # Get Streak 
        streak_check_result = invoke_http(f"{streak_URL}/{streak_id}", method='GET')
        print("streak", streak_check_result)
        if (streak_check_result["code"] != 200):
            streak_by_goal = invoke_http(f"{streak_URL}s/{goal_id}", method='GET')
            # print("get streaks by goal", streak_by_goal)
            if (streak_by_goal["code"] == 200):
                streak_id = streak_by_goal["data"][0]["streak_id"]
                # print("updated streak id", streak_id)

        coinEarned = 0
        streak_json = {}
        goal_met = False
        to_prompt = False
        
        iso_current_week = datetime.date(datetime.now()).isocalendar()[1]
        streak_week_current = streak_check_result["data"]["week_current"]
        streak_result =  streak_check_result["data"]

        # new week from last updated week
        if streak_week_current + 1 == iso_current_week:
            # moderate activity threshold - MET level = 3
            # if goal is met upon refresh
            if (estimated_met >= 3) and (goal_result["target"]):
                streak_count = streak_result["streak_count"] + 1
                streak_json = {
                    "streak_id": streak_result["streak_id"],
                    "goal_id": streak_result["goal_id"],
                    "week_started": streak_result["week_started"],
                    "week_current": iso_current_week,
                    "streak_count": streak_count
                    }
                coinEarned = 10 + streak_count * 5
                goal_met = True
                to_prompt = True
            else:
                # no change as week is still onoging
                streak_json = {
                    "streak_id": streak_result["streak_id"],
                    "goal_id": streak_result["goal_id"],
                    "week_started": streak_result["week_started"],
                    "week_current": streak_result["week_current"],
                    "streak_count": streak_result["streak_count"]
                }
                coinEarned = 0
                    
        # when goal is first set by user
        elif streak_week_current == 0:
            if (estimated_met >= 3) and (goal_result["target"]):
                streak_json = {
                    "streak_id": streak_result["streak_id"],
                    "goal_id": streak_result["goal_id"],
                    "week_started": iso_current_week,
                    "week_current": iso_current_week,
                    "streak_count": 1
                    }
                coinEarned = 10 + streak_count * 5
                goal_met = True
                to_prompt = True
            else:
                # no prompt as streak has not been achieved before
                streak_json = {
                    "streak_id": streak_result["streak_id"],
                    "goal_id": streak_result["goal_id"],
                    "week_started": iso_current_week,
                    "week_current": 0,
                    "streak_count": 0
                }
                coinEarned = 0

        # week_current is current week
        elif streak_week_current == iso_current_week:
            # no change as goal has already been met for this week
            streak_json = {
                "streak_id": streak_result["streak_id"],
                "goal_id": streak_result["goal_id"],
                "week_started": streak_result["week_started"],
                "week_current": streak_result["week_current"],
                "streak_count": streak_result["streak_count"],
            }
            coinEarned = 0

        # streak is broken (> 1 from week_current; reset at the end of the week)    
        else:
            streak_json = {
                "streak_id": streak_result["streak_id"],
                "goal_id": streak_result["goal_id"],
                "week_started": iso_current_week,
                "week_current": iso_current_week,
                "streak_count": 0
            }
            coinEarned = 0
            goal_met = False
            to_prompt = True

        streak_update_result = invoke_http(f"{streak_URL}/{streak_id}", method='PUT', json=streak_json)
        print("streak update", streak_update_result)

        # create a new coin transaction
        if coinEarned > 0:
            coin_json = {
                "user_id": user_id,
                "points_earned": coinEarned,
                "earned_date": datetime.now().isoformat(),
                "source": "streak"
            }
            coin_result = invoke_http(f"{coin_URL}", method='POST', json=coin_json)
            print(coin_result)
            
            user_result = invoke_http(f"{user_URL}/id/{user_id}", method='GET')
            user_email = user_result["data"]["email"]
            user_total_coin = user_result["data"]["total_point"]
            
            print(user_total_coin + coinEarned)

            # update user's coins
            user_json = {
                "total_point": user_total_coin + coinEarned
            }
        
            user_result = invoke_http(f"{user_URL}/{user_email}", method='PATCH', json=user_json)

        # return {"code": [met_result, streak_update_result]}
        return {
            "code": 200,
            "data": {
                "daily_time_lapse": met_result['daily_time_lapse'],
                "monthly_top_activity": met_result['monthly_top_activity'],
                "monthly_time_lapse": met_result['monthly_time_lapse'],
                "weekly_time_lapse": met_result['weekly_time_lapse'],
                "streak_count": streak_update_result["data"]['streak_count'],
                "week_started": streak_update_result["data"]['week_started'],
                "week_current": streak_update_result["data"]['week_current'],
                "activities_in_month": met_result['activities_in_month'],
                "monthly_distance": met_result['monthly_distance'],
                "goal_met": goal_met,
                "to_prompt": to_prompt
            }
        }, 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": str(e)
        }), 500

# if __name__ == '__main__':
#     app.run(port=5030, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
        