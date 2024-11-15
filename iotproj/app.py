from flask import Flask, render_template, request, jsonify
import numpy as np
import time
import json
from datetime import datetime

app = Flask(__name__)

# Firebase Initialization (commented out for simplicity)
# cred = credentials.Certificate("firebase_credentials.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://iot-project-13254-default-rtdb.firebaseio.com'
# })

# HiveMQ broker settings
HIVEMQ_BROKER = "broker.hivemq.com"  # Public broker for testing
HIVEMQ_PORT = 1883
HIVEMQ_TOPIC = "iot/data"

# Define threshold values for anomaly detection
THRESHOLDS = {
    "vibration": 8.0,
    "temperature": 80.0,
    "pressure": 110.0,
    "rpm": 1500,
    "oil_level": 20,
    "battery_status": 10
}

# Function to simulate sensor data with additional parameters
def simulate_sensor_data():
    vibration = np.random.normal(loc=5, scale=1)
    temperature = np.random.normal(loc=70, scale=2)
    pressure = np.random.normal(loc=100, scale=5)
    rpm = np.random.normal(loc=1200, scale=100)
    oil_level = max(0, np.random.normal(loc=80, scale=5))
    battery_status = max(0, np.random.normal(loc=100, scale=1))

    # Gradual wear simulation
    vibration += np.random.normal(scale=0.05)
    temperature += np.random.normal(scale=0.02)
    pressure += np.random.normal(scale=0.03)

    return {
        "device_id": "IoT7",  # Simulating device_id
        "timestamp": int(time.time()),
        "vibration": round(vibration, 2),
        "temperature": round(temperature, 2),
        "pressure": round(pressure, 2),
        "rpm": round(rpm, 2),
        "oil_level": round(oil_level, 2),
        "battery_status": round(battery_status, 2)
    }

# Function to check for anomalies based on thresholds
def check_for_anomalies(data):
    anomalies = {}
    for key, threshold in THRESHOLDS.items():
        if data[key] > threshold:
            anomalies[key] = data[key]
    return anomalies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    max_iterations = int(request.form.get('max_iterations'))
    iteration_count = 0
    result_data = []
    while iteration_count < max_iterations:
        # Simulate data
        data = simulate_sensor_data()
        anomalies = check_for_anomalies(data)
        
        result_data.append({
            "data": data,
            "anomalies": anomalies,
            "iteration": iteration_count + 1
        })
        
        iteration_count += 1
        time.sleep(1)  # Sleep interval before next iteration

    return render_template('index.html', result_data=result_data, max_iterations=max_iterations)

if __name__ == '__main__':
    app.run(debug=True)
