from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from .user import User
from flask_cors import CORS, cross_origin

from datetime import datetime, timedelta, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/healthpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)
CORS(app)

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

# Create a new event
@app.route('/event', methods=['POST'])
def create_event():
    data = request.json
    new_event = Event(
        title=data.get('title'),
        second_title=data.get('second_title'),
        description=data.get('description'),
        location=data.get('location'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d %H:%M:%S'),
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d %H:%M:%S'),
        organiser=data.get('organiser'),
        event_type=data.get('event_type'),
        max_signups=data.get('max_signups'),
        current_signups=data.get('current_signups', 0),
        mode=data.get('mode'),
        participant_remark=data.get('participant_remark'),
        entry_code=data.get('entry_code'),
        event_point=data.get('event_point'),
        event_program=data.get('event_program'),
        tier=data.get('tier'),
        organiser_phone=data.get('organiser_phone'),
        organiser_email=data.get('organiser_email')
    )
    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.json() for event in events]), 200

# Get an event by ID
@app.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.json()), 200
    return jsonify({"error": "Event not found"}), 404

# Update an event by ID
@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event:
        data = request.json
        event.title = data.get('title', event.title)
        event.second_title = data.get('second_title', event.second_title)
        event.description = data.get('description', event.description)
        event.location = data.get('location', event.location)
        event.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d %H:%M:%S')
        event.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d %H:%M:%S')
        event.organiser = data.get('organiser', event.organiser)
        event.event_type = data.get('event_type', event.event_type)
        event.max_signups = data.get('max_signups', event.max_signups)
        event.current_signups = data.get('current_signups', event.current_signups)
        event.mode = data.get('mode', event.mode)
        event.participant_remark = data.get('participant_remark', event.participant_remark)
        event.entry_code = data.get('entry_code', event.entry_code)
        event.event_point = data.get('event_point', event.event_point)
        event.event_program = data.get('event_program', event.event_program)
        event.tier = data.get('tier', event.tier)
        event.organiser_phone = data.get('organiser_phone', event.organiser_phone)
        event.organiser_email = data.get('organiser_email', event.organiser_email)

        try:
            db.session.commit()
            return jsonify(event.json()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Event not found"}), 404

# Delete an event by ID
@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        try:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Event not found"}), 404

# Get available events 
@app.route('/event/available', methods=['GET'])
def get_available_events():
    try:
        events = Event.query.all()

        if events:
            available_events = []
            current = datetime.now()

            for event in events:
                # Check for event capacity
                if event.current_signups < event.max_signups:

                    # Check for event date and time > 1 hour from now
                    if current < event.start_date and (event.start_date - current).total_seconds() > 3600:
                        available_events.append(event)
                    
            if available_events:
                return jsonify([
                    event.json() for event in available_events
                ]), 200

            else:
                return jsonify({
                    "code": 400, 
                    "message": "No available events"
                }), 400
        
        return jsonify({
            "code": 400,
            "message": "No events found"
        }), 400
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
