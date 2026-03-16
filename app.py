from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ── Users ─────────────────────────────────────────────────────────────────────
users = {
    'admin':   {'password': 'admin123',   'role': 'admin'},
    'student': {'password': 'student123', 'role': 'student'}
}

# ── In-memory data ────────────────────────────────────────────────────────────
events = [
    {'id': 1, 'name': 'Tech Symposium 2026',   'date': '2026-04-10', 'venue': 'Main Auditorium',  'seats': 100, 'registered': 0},
    {'id': 2, 'name': 'Cultural Fest',          'date': '2026-04-15', 'venue': 'Open Air Theatre', 'seats': 200, 'registered': 0},
    {'id': 3, 'name': 'Hackathon 2026',         'date': '2026-04-20', 'venue': 'CS Lab Block',     'seats': 50,  'registered': 0},
    {'id': 4, 'name': 'Career Fair',            'date': '2026-05-05', 'venue': 'Conference Hall',  'seats': 150, 'registered': 0},
]

registrations = []
next_event_id = 5
next_reg_id   = 1

# ── Serve frontend ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ── POST /api/login ───────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    user = users.get(username)
    if user and user['password'] == password:
        return jsonify({'success': True, 'username': username, 'role': user['role']})
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

# ── GET /api/events ───────────────────────────────────────────────────────────
@app.route('/api/events', methods=['GET'])
def get_events():
    result = []
    for ev in events:
        result.append({
            'id':         ev['id'],
            'name':       ev['name'],
            'date':       ev['date'],
            'venue':      ev['venue'],
            'seats':      ev['seats'],
            'registered': ev['registered'],
            'available':  ev['seats'] - ev['registered']
        })
    return jsonify({'events': result})

# ── POST /api/events (admin only) ─────────────────────────────────────────────
@app.route('/api/events', methods=['POST'])
def add_event():
    global next_event_id
    data = request.get_json()
    if not data.get('name') or not data.get('date') or not data.get('venue') or not data.get('seats'):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    new_event = {
        'id':         next_event_id,
        'name':       data['name'],
        'date':       data['date'],
        'venue':      data['venue'],
        'seats':      int(data['seats']),
        'registered': 0
    }
    events.append(new_event)
    next_event_id += 1
    return jsonify({'success': True, 'event': new_event}), 201

# ── DELETE /api/events/<id> (admin only) ──────────────────────────────────────
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events, registrations
    original = len(events)
    events = [e for e in events if e['id'] != event_id]
    if len(events) < original:
        registrations = [r for r in registrations if r['event_id'] != event_id]
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Event not found'}), 404

# ── POST /api/events/<id>/register ────────────────────────────────────────────
@app.route('/api/events/<int:event_id>/register', methods=['POST'])
def register(event_id):
    global next_reg_id
    data  = request.get_json()
    name  = data.get('name', '').strip()
    email = data.get('email', '').strip()
    if not name or not email:
        return jsonify({'success': False, 'message': 'Name and email are required'}), 400
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return jsonify({'success': False, 'message': 'Event not found'}), 404
    if event['registered'] >= event['seats']:
        return jsonify({'success': False, 'message': 'No seats available'}), 400
    already = any(r for r in registrations if r['event_id'] == event_id and r['email'] == email)
    if already:
        return jsonify({'success': False, 'message': 'This email is already registered for this event'}), 400
    event['registered'] += 1
    new_reg = {
        'id':         next_reg_id,
        'event_id':   event_id,
        'event_name': event['name'],
        'name':       name,
        'email':      email
    }
    registrations.append(new_reg)
    next_reg_id += 1
    return jsonify({'success': True, 'registration': new_reg}), 201

# ── GET /api/registrations ────────────────────────────────────────────────────
@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    return jsonify({'registrations': registrations, 'total': len(registrations)})

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
