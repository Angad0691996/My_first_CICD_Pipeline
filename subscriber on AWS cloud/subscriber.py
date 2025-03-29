import os
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core Details
ENDPOINT = "axpjfhduaw82h-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "angad_subscriber"
TOPIC = "vehicle/data"

# Absolute Paths to Certificates
ROOT_CA = os.path.abspath("AmazonRootCA1.pem")
PRIVATE_KEY = os.path.abspath("private.key")
CERTIFICATE = os.path.abspath("device_certificate.crt")

# Initialize MQTT Client
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)

# Callback function when message is received
def message_callback(client, userdata, message):
    print("\n🚗 Received Data:")
    print(json.dumps(json.loads(message.payload), indent=4))

# Connect & Subscribe
mqtt_client.connect()
print(f"Connected to AWS IoT Core. Subscribing to topic: {TOPIC}...")
mqtt_client.subscribe(TOPIC, 1, message_callback)

# Keep listening for messages
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nSubscriber stopped.")

