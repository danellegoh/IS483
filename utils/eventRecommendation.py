from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)
CORS(app)

class User(db.Model):    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(64), nullable = False)
    height = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    contact_details = db.Column(db.String(64), nullable = False)
    nationality = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(64), nullable = False, unique = True)
    location_group = db.Column(db.String(64), nullable = False)
    school = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(64), nullable = False) 
    parent_id = db.Column(db.String(64), db.ForeignKey('user_id'), nullable = True) 
    role = db.Column(db.String(64), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False)
    last_login = db.Column(db.DateTime, nullable = False)
    total_point = db.Column(db.Integer, nullable = False)
    health_tier = db.Column(db.Integer, nullable = False)
    goal_user = db.relationship('Goal', backref='user', lazy=True)

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
        
# Flask route to get user information by ID
@app.route('/user/id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "location_group": user.location_group,
            "school": user.school,
            "health_tier": user.health_tier
        }
        return jsonify({"code": 200, "data": user_data}), 200
    return jsonify({"code": 404, "error": "User not found"}), 404


def map_location_to_group(location):
    location_map = {
        "North": [
            "woodlands", "yishun", "sembawang", "canberra", "khatib", 
            "admiralty", "yio chu kang", "ang mo kio"
        ],
        "East": [
            "bedok", "changi", "pasir ris", "tampines", "simei", "loyang", 
            "paya lebar", "upper changi"
        ],
        "South": [
            "sentosa", "marina bay", "bukit merah", "harbourfront", 
            "telok blangah", "tanjong pagar", "keppel"
        ],
        "West": [
            "jurong west", "jurong east", "clementi", "bukit batok", 
            "choa chu kang", "bukit panjang", "tengah", "boon lay", "tuas"
        ],
        "Central": [
            "orchard", "novena", "dhoby ghaut", "bencoolen", "newton", 
            "queenstown", "tiong bahru", "bukit timah", "kallang", 
            "toa payoh", "bendemeer", "rochor", "city hall"
        ],
        "Northeast": [
            "sengkang", "punggol", "serangoon", "hougang", "kovan", 
            "buangkok", "compassvale", "fernvale"
        ]
    }

    location = location.lower().strip()
    for group, locations in location_map.items():
        if location in locations:
            return group
    return None 



@app.route('/user/<int:user_id>/eligible-events', methods=['GET'])
def get_eligible_events(user_id):
    #get user data
    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "error": "User not found"}), 404
    
    #get all event data
    events = Event.query.all()
    eligible_event_ids = []

    current_date = datetime.now()

    #condition based event filtering
    for event in events:
        event_location_group = map_location_to_group(event.location)

        try:
            # Convert event.start_date to datetime if it's in string format
            if isinstance(event.start_date, str):
                event_start_date = datetime.strptime(event.start_date, '%d/%m/%Y %H:%M:%S')
            else:
                event_start_date = event.start_date  # Already a datetime object

            #1. check that event is existing
            if (event_start_date < current_date and
                #2. check that event has slots for signing up
                int(event.current_signups) < int(event.max_signups) and
                #3. check that event tier matches user health tier
                int(event.tier) == int(user.health_tier) and
                #4 event location matches user location group
                event_location_group.lower() == user.location_group.lower()):
                # Collect only the event_id of eligible events
                eligible_event_ids.append(event.event_id)

        except ValueError as e:
            return jsonify({"code": 500, "error": f"Date format error: {str(e)}"}), 500

    # Return the list of eligible event IDs
    return jsonify({"code": 200, "data": eligible_event_ids}), 200


