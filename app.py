# app.py
# from flask import Flask, render_template, jsonify
# from flask_socketio import SocketIO, emit
# import json
# from datetime import datetime
# import random
# from threading import Thread
# import time
# from pymongo import MongoClient, errors# app.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
from datetime import datetime
import random
from threading import Thread
import time
from pymongo import MongoClient, errors
import certifi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# mongo_uri = 'mongodb+srv://hackathon:yaHAVKDwVLgNEFVN@cluster0.eer9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
# mongo_uri = 'mongodb+srv://hackathon:yaHAVKDwVLgNEFVN@cluster0.eer9i.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'
mongo_uri = "mongodb+srv://hackathon:yaHAVKDwVLgNEFVN@cluster0.eer9i.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_ca_certs=" + certifi.where()


try:
    mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    print("Connected to MongoDB!")
    db = mongo_client['face_recognition']
    

except errors.ServerSelectionTimeoutError as err:
    print("Could not connect to MongoDB. Server selection timeout error:", err)
except errors.ConnectionError as err:
    print("Connection error:", err)
except Exception as err:
    print("An error occurred:", err)

    access_log_collection = db['access_logs']

latest_data = {
    'motion': {},
    'door': {},
    'window': {},
    'camera': {},
    'environmental': {}
}

def generate_sensor_data():
    while True:
        motion_data = {
            'type': 'motion',
            'location': random.choice(['Living Room', 'Kitchen', 'Hallway', 'Garage', 'Master Bedroom']),
            'detected': random.random() < 0.3,
            'timestamp': datetime.now().isoformat()
        }
        latest_data['motion'] = motion_data
        socketio.emit('sensor_update', motion_data)

        door_data = {
            'type': 'door',
            'location': random.choice(['Front Door', 'Back Door', 'Garage Door', 'Patio Door']),
            'status': 'open' if random.random() < 0.2 else 'closed',
            'timestamp': datetime.now().isoformat()
        }
        latest_data['door'] = door_data
        socketio.emit('sensor_update', door_data)

        window_data = {
            'type': 'window',
            'location': random.choice(['Living Room Window', 'Kitchen Window', 'Bedroom Window 1', 'Bedroom Window 2']),
            'status': 'open' if random.random() < 0.1 else 'closed',
            'timestamp': datetime.now().isoformat()
        }
        latest_data['window'] = window_data
        socketio.emit('sensor_update', window_data)

        env_data = {
            'type': 'environmental',
            'temperature': round(random.uniform(60, 85), 1),
            'humidity': round(random.uniform(30, 70)),
            'smoke_detected': random.random() < 0.01,
            'co_detected': random.random() < 0.005,
            'timestamp': datetime.now().isoformat()
        }
        latest_data['environmental'] = env_data
        socketio.emit('sensor_update', env_data)

        camera_data = {
            'type': 'camera',
            'location': random.choice(['Front Door Camera', 'Backyard Camera', 'Garage Camera']),
            'event': random.choice(['Motion Detected', 'Person Detected', 'Vehicle Detected', 'Clear']),
            'timestamp': datetime.now().isoformat()
        }
        latest_data['camera'] = camera_data
        socketio.emit('sensor_update', camera_data)

        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current-state')
def get_current_state():
    return jsonify(latest_data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('sensor_update', latest_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/api/access-logs', methods=['GET'])
def get_access_logs():
    logs = list(access_log_collection.find())
    formatted_logs = [
        {
            '_id': str(log['_id']),
            'timestamp': log.get('timestamp'),
            'status': log.get('status'),
            'user_name': log.get('user_name')
        }
        for log in logs
    ]
    return jsonify(formatted_logs)

if __name__ == '__main__':
    sensor_thread = Thread(target=generate_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)



# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins="*")

# mongo_uri = 'mongodb+srv://hackathon:yaHAVKDwVLgNEFVN@cluster0.eer9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# try:
#     # Create a MongoDB client
#     mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
#     # Attempt to ping the server to check connectivity
#     mongo_client.admin.command('ping')
    
#     print("Connected to MongoDB!")
    
#     # Access the database and collection
#     db = mongo_client['face_recognition']
#     access_log_collection = db['access_logs']

# except errors.ServerSelectionTimeoutError as err:
#     print("Could not connect to MongoDB. Server selection timeout error:", err)
# except errors.ConnectionError as err:
#     print("Connection error:", err)
# except Exception as err:
#     print("An error occurred:", err)

# # Store latest sensor data
# latest_data = {
#     'motion': {},
#     'door': {},
#     'window': {},
#     'camera': {},
#     'environmental': {}
# }

# def generate_sensor_data():
#     """Simulate sensor data generation (replace with actual Node-RED data)"""
#     while True:
#         # Motion sensor
#         motion_data = {
#             'type': 'motion',
#             'location': random.choice(['Living Room', 'Kitchen', 'Hallway', 'Garage', 'Master Bedroom']),
#             'detected': random.random() < 0.3,
#             'timestamp': datetime.now().isoformat()
#         }
#         latest_data['motion'] = motion_data
#         socketio.emit('sensor_update', motion_data)

#         # Door sensor
#         door_data = {
#             'type': 'door',
#             'location': random.choice(['Front Door', 'Back Door', 'Garage Door', 'Patio Door']),
#             'status': 'open' if random.random() < 0.2 else 'closed',
#             'timestamp': datetime.now().isoformat()
#         }
#         latest_data['door'] = door_data
#         socketio.emit('sensor_update', door_data)

#         # Window sensor
#         window_data = {
#             'type': 'window',
#             'location': random.choice(['Living Room Window', 'Kitchen Window', 'Bedroom Window 1', 'Bedroom Window 2']),
#             'status': 'open' if random.random() < 0.1 else 'closed',
#             'timestamp': datetime.now().isoformat()
#         }
#         latest_data['window'] = window_data
#         socketio.emit('sensor_update', window_data)

#         # Environmental sensor
#         env_data = {
#             'type': 'environmental',
#             'temperature': round(random.uniform(60, 85), 1),
#             'humidity': round(random.uniform(30, 70)),
#             'smoke_detected': random.random() < 0.01,
#             'co_detected': random.random() < 0.005,
#             'timestamp': datetime.now().isoformat()
#         }
#         latest_data['environmental'] = env_data
#         socketio.emit('sensor_update', env_data)

#         # Camera data
#         camera_data = {
#             'type': 'camera',
#             'location': random.choice(['Front Door Camera', 'Backyard Camera', 'Garage Camera']),
#             'event': random.choice(['Motion Detected', 'Person Detected', 'Vehicle Detected', 'Clear']),
#             'timestamp': datetime.now().isoformat()
#         }
#         latest_data['camera'] = camera_data
#         socketio.emit('sensor_update', camera_data)

#         time.sleep(5)  # Update every 5 seconds

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/current-state')
# def get_current_state():
#     return jsonify(latest_data)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     emit('sensor_update', latest_data)

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @app.route('/api/access-logs', methods=['GET'])
# def get_access_logs():
#     """Fetch access logs from MongoDB"""
#     logs = list(access_log_collection.find())  # Fetch all access logs
#     # Transform the logs to include only the needed fields and convert _id to string
#     formatted_logs = [
#         {
#             '_id': str(log['_id']),  # Convert ObjectId to string
#             'timestamp': log.get('timestamp'),
#             'status': log.get('status'),
#             'user_name': log.get('user_name')
#         }
#         for log in logs
#     ]
#     print(formatted_logs)
#     return jsonify({formatted_logs})

# if __name__ == '__main__':
#     # Start the sensor simulation in a background thread
#     sensor_thread = Thread(target=generate_sensor_data)
#     sensor_thread.daemon = True
#     sensor_thread.start()
    
#     # Run the Flask application
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)
