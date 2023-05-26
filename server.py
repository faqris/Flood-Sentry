import paho.mqtt.client as paho
from paho import mqtt
from flask import Flask, request
from influxdb import InfluxDBClient
import threading

app = Flask(__name__)

# MQTT Broker Configuration
mqtt_broker = 'a5da1b92468e4cd6b6dd31c7909a5cc6.s2.eu.hivemq.cloud'
mqtt_port = 8883
mqtt_topic = 'floodsentry'
mqtt_username = 'admin'
mqtt_password = 'Admin1234'

# InfluxDB Configuration
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = 'floodsentry'

@app.route("/")
def index():
    return "Flood Sentry"
    
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("MQTT Topic Subscribed: " + str(mid))

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + " " + str(msg.payload))
    save_to_influxdb(msg.topic, msg.payload)
    
# Start the MQTT client in a separate thread
def mqtt_thread():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_broker, mqtt_port)

    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.subscribe(mqtt_topic + "/#", qos=1)
    client.publish(mqtt_topic + "/ultrasonic", payload="0", qos=1)
    client.loop_forever()
        
def save_to_influxdb(topic, payload):
    try:
        client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
        client.create_database(INFLUXDB_DATABASE)
        client.switch_database(INFLUXDB_DATABASE)
        data_point = {
            "measurement": "ultrasonic",
            "tags": {
                "topic": topic
            },
            "fields": {
                "value": float(payload)
            }
        }
        client.write_points([data_point])
        print("Successfully stored in InfluxDB:", data_point)
    except Exception as e:
        print("Error storing data in InfluxDB:", str(e))

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=mqtt_thread)
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=5000)
