import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta, date

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

class Event(db.Model):
    __tablename__ = 'events'
    
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    second_title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    organiser = db.Column(db.String(64), nullable=False)
    event_type = db.Column(db.String(64), nullable=False)
    # created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    max_signups = db.Column(db.Integer, nullable=False)
    current_signups = db.Column(db.Integer, nullable=False, default=0)
    mode = db.Column(db.String(64), nullable=False)
    participant_remark = db.Column(db.String(200), nullable=False)
    entry_code = db.Column(db.String(64), nullable=True)
    event_point = db.Column(db.Integer, nullable=False)
    event_program = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    organiser_phone = db.Column(db.String(64), nullable=False)
    organiser_email = db.Column(db.String(64), nullable=False)

    def __init__(self, title, second_title, description, location, start_date, end_date, organiser, event_type, max_signups, mode, participant_remark, entry_code, event_point, event_program, tier, organiser_phone, organiser_email, current_signups=0):
        self.title = title
        self.second_title = second_title
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.organiser = organiser
        self.event_type = event_type
        # self.created_by = created_by
        self.max_signups = max_signups
        self.current_signups = current_signups
        self.mode = mode
        self.participant_remark = participant_remark
        self.entry_code = entry_code
        self.event_point = event_point
        self.event_program = event_program
        self.tier = tier
        self.organiser_phone = organiser_phone
        self.organiser_email = organiser_email

    def json(self):
        return {
            "event_id": self.event_id,
            "title": self.title,
            "second_title": self.second_title,
            "description": self.description,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "organiser": self.organiser,
            "event_type": self.event_type,
            # "created_by": self.created_by,
            "created_date": self.created_date.isoformat(),
            "max_signups": self.max_signups,
            "current_signups": self.current_signups,
            "mode": self.mode,
            "participant_remark": self.participant_remark,
            "entry_code": self.entry_code,
            "event_point": self.event_point,
            "event_program": self.event_program,
            "tier": self.tier,
            "organiser_phone": self.organiser_phone,
            "organiser_email": self.organiser_email
        }

def map_location_to_group(location):
    location_map = {
        "North": [
            "woodlands", "woodlands north", "woodlands south", "yishun", "sembawang", "canberra", 
            "khatib", "admiralty", "yio chu kang", "ang mo kio", "marsiling", "springleaf", 
            "lentor", "mayflower", "bright hill", "upper thomson", "tagore"
        ],
        "East": [
            "bedok", "changi", "pasir ris", "tampines", "simei", "loyang", "paya lebar", 
            "upper changi", "eunos", "kembangan", "tanah merah", "expo", "changi airport", 
            "dakota", "mountbatten", "ubis", "geylang bahru", "tampines east", "tampines west", 
            "bedok north", "bedok reservoir", "kaki bukit", "ubi", "tai seng", "macpherson", 
            "aljunied", "paya lebar"
        ],
        "South": [
            "sentosa", "marina bay", "bukit merah", "harbourfront", "telok blangah", "tanjong pagar", 
            "keppel", "downtown", "raffles place", "outram park", "marina south pier", "gardens by the bay", 
            "fort canning", "maxwell", "telok ayer", "bayfront", "marina bay sands", "marina barrage"
        ],
        "West": [
            "jurong west", "jurong east", "clementi", "bukit batok", "choa chu kang", "bukit panjang", 
            "tengah", "boon lay", "tuas", "pioneer", "lakeside", "joo koon", "gul circle", 
            "haw par villa", "one north", "buona vista", "dover", "kent ridge", "clementi west", 
            "jalan bahar", "jurong pier"
        ],
        "Central": [
            "orchard", "novena", "dhoby ghaut", "bencoolen", "newton", "queenstown", "tiong bahru", 
            "bukit timah", "kallang", "toa payoh", "bendemeer", "rochor", "city hall", "somerset", 
            "bugis", "promenade", "farrer park", "jalan besar", "little india", "braddell", 
            "redhill", "commonwealth", "stamford", "keong saik", "golden mile", "bras basah", 
            "botanic gardens", "clarke quay", "esplanade", "raffles quay", "chinatown", 
            "great world", "havelock", "holland village", "tan kah kee", "farrer road", "caldecott", 
            "stevens", "napier", "orchard boulevard", "havelock road", "goldhill plaza", "bukit ho swee"
        ]
    }

    location = location.lower().strip()
    for group, locations in location_map.items():
        if location in locations:
            return group
    return None 

@app.route('/user/<int:user_id>/eligible-events', methods=['GET'])
def get_eligible_events(user_id):
    # Get user data
    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "error": "User not found"}), 404

    user_location_group = map_location_to_group(user.location_group)

    if not user_location_group:
        return jsonify({"code": 400, "error": "User location group not recognized"}), 400

    events = Event.query.all()
    eligible_event_ids = []

    current_date = datetime.now()

    for event in events:
        event_location_group = map_location_to_group(event.location)
        
        if not event_location_group:
            continue

        try:
            # Convert event.start_date to datetime if it's in string format
            if isinstance(event.start_date, str):
                event_start_date = datetime.strptime(event.start_date, '%Y-%m-%d %H:%M:%S')  # Update format if needed
            else:
                event_start_date = event.start_date  # Already a datetime object

            # Check conditions:
            # 1. Event start date is in the future
            # 2. Event has available slots for signing up
            # 3. Event tier matches user health tier
            # 4. Event location group matches user's location group
            if (event_start_date > current_date and
                int(event.current_signups) < int(event.max_signups) and
                int(event.tier) == int(user.health_tier) and
                event_location_group == user_location_group):
                
                # Collect only the event_id of eligible events
                eligible_event_ids.append(event.event_id)

        except ValueError as e:
            return jsonify({"code": 500, "error": f"Date format error: {str(e)}"}), 500

    # Return the list of eligible event IDs
    return jsonify({"code": 200, "data": eligible_event_ids}), 200

# if __name__ == '__main__':
#     app.run(port=5042, debug=True)
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')


