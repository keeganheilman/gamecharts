from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


DB_USERNAME = 'gamecharts'
DB_PASSWORD = 'gamecharts'
DB_NAME = 'gc'
DB_HOST = 'localhost'
DB_PORT = '5432'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db = SQLAlchemy(app)

# create Event class as inherited db.Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Event: {self.description}'

    def __init__(self, description):
        self.description = description

# format the event
def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }


#  create Event instance with description
@app.route('/events', methods = ['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# retrieve all events
@app.route('/events', methods = ['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

# retrieve single event by id
@app.route('/events/<id>', methods = ['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).first()
    formatted_event = format_event(event)
    return {'events': [formatted_event]}


# delete an event by id
@app.route('/events/<id>', methods = ['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    return f"Event (id: {id}) deleted"


@app.route('/events/<id>', methods = ['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description=description, created_at = datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}

@app.route('/')
def hello():
    return 'Hello World.'


if __name__ == '__main__    ':
    app.run()
