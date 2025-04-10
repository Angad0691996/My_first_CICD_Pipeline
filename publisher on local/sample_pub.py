import os
import random  # Import the random module
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time

# AWS IoT Core Details
ENDPOINT = "axpjfhduaw82h-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "angad_publisher"
TOPIC = "vehicle/data"

# Absolute Paths to Certificates
ROOT_CA = os.path.abspath("AmazonRootCA1.pem")
PRIVATE_KEY = os.path.abspath("private.key")
CERTIFICATE = os.path.abspath("device certificate.crt")

# Initialize MQTT Client
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)

# Connect to AWS IoT Core
mqtt_client.connect()
print("Connected to AWS IoT Core.")

# Function to Generate Random Vehicle Data
def generate_vehicle_data():
    return {
        "Vehicle_ID":"MH12VC1893",
        "Type":"SUV",
        "FUEL":"PETROL",
        "SPEED":"111KMPH"

    }

# Publish Data Every 5 Seconds
# Loop to send random data continuously
while True:
    vehicle_data = generate_vehicle_data()
    payload = json.dumps(vehicle_data)
    mqtt_client.publish(TOPIC, payload, 1)
    print(f"Published: {payload}")

    time.sleep(5)  # Send data every 5 seconds

# Disconnect (if needed)
# mqtt_client.disconnect()
# print("Disconnected.")
