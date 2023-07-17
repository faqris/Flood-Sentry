# Flood Sentry
### Software Engineering (SEEL4213)
#### Group: Rampaging Rhinos
##### Team Member: 
##### 1. Muhammad Faqris Bin Kamaruzaman
##### 2. Muhammad Hazril bin Zakaria
##### 3. Nurul Ain Nabila Binti Ismail

1.0 Problem Statement

The frequent occurrence of floods in low-lying areas poses a significant threat to life and property. Traditional flood detection methods are often limited in scope, accuracy, and timeliness. There is a need for a reliable and efficient flood detection system that can alert people in advance of an impending flood and help them take appropriate measures to minimize the damage. The goal of this project is to develop a flood detection system that uses sensors, a cloud platform, and a dashboard to detect floods in real-time, generate alerts, and provide users with critical information to mitigate the impact of floods.

2.0 System Architecture

The system architecture consists of a ultrasonic HC-SR04 sensor that sends data to a microcontroller, which is NodeMCU ESP32. It connects to a Mosquitto MQTT broker and sends the data via wifi. A Python Flask application run on a server hosted on PythonAnywhere subscribes to the MQTT broker, receives the data and stores it to an InfluxDB database. Grafana reads the data from the InfluxDB database and visualizes it in real-time dashboards. The dashboard is accessible to users via a public URL that is hosted on the PythonAnywhere cloud platform.

3.0 Sensor 
3.1 Nodemcu ESP32

The NodeMCU ESP32 is a microcontroller that is ideal for the flood detection system. It features built-in WiFi and Bluetooth capabilities, making it easy to connect to the cloud platform and communicate with other devices. With its low power consumption and small form factor, the NodeMCU ESP32 is perfect for use in remote areas where power may be limited. To measure water level, sensors can be connected to the microcontroller for data collection to perform real-time analysis. This allowed for immediate detection and alert notifications.

3.2 Ultrasonic HC-SR04

The HC-SR04 is an ultrasonic sensor that can be used as a water level sensor to measure the distance between the sensor and the water surface. It can determine the water level in real-time by emitting high-frequency sound waves and measuring the time taken for the echo to bounce back. It consists of a transmitter and a receiver module, which can detect objects within a range of 2cm to 400cm with an accuracy of up to 3mm. 

3.3 MQTT
MQTT (Message Queuing Telemetry Transport) is a lightweight, open-source messaging protocol that is ideal for use in IoT (Internet of Things) applications. It can be used to establish a connection between the NodeMCU ESP32 microcontroller and PythonAnywhere cloud platform.

4.0 Cloud Platform

4.1 PythonAnywhere
PythonAnywhere allows users to write and run Python code in the cloud, which is particularly useful for IoT projects that require a persistent and reliable connection. Additionally, PythonAnywhere provides a range of pre-installed libraries and packages, including those for IoT-related tasks such as data processing and visualization. It also has support for many popular IoT hardware devices, making it easy to interface with sensors and other devices. Finally, PythonAnywhere offers a simple user interface making it easy to manage and deploy IoT applications. 

![Sample pic](https://raw.githubusercontent.com/faqris/Flood-Sentry/d15fad84682bb7dcd19f532f003de43597b7c614/img/Screenshot%202023-07-18%20002020.png)
Porting flask app from stage 1 to PythonAnywhere 

5.0 Dashboard
5.1 Grafana
Grafana is an open-source platform that allows users to visualize and analyze data from multiple sources through interactive and customizable dashboards. A Grafana dashboard is a collection of panels that display metrics and data in a visual format such as graphs, tables, and gauges. The dashboard can be customized according to the user's needs. Grafana also supports a wide range of data sources, databases, cloud services, and APIs. Thus, making it a versatile tool for monitoring and analyzing systems and applications.

5.2 User Interface
![Sample pic](https://raw.githubusercontent.com/faqris/Flood-Sentry/0e599119b4f5251d5c44c7812bf1c271a23690c5/grafana%20dashboard.jpg)

![Sample pic](https://raw.githubusercontent.com/faqris/Flood-Sentry/0e599119b4f5251d5c44c7812bf1c271a23690c5/mhive.jpg)
system architecture by using hive mqtt
![Sample pic](https://raw.githubusercontent.com/faqris/Flood-Sentry/0e599119b4f5251d5c44c7812bf1c271a23690c5/postgresql%20database%20table%20ultrasonic%20dgn%20water%20level.jpg)
postgresql database table ultrasonic with water level

6.0 Discussion
The flood detection system being proposed demonstrates a notable improvement over conventional methods and presents multiple benefits. The system employs sensors to enable continuous monitoring of water levels, thereby facilitating real-time data acquisition for flood detection. The cloud platform facilitates centralized data processing and analysis, thereby enabling accurate and timely alerts. Furthermore, the dashboard, designed with a focus on user-friendliness, guarantees convenient access to information and enhances its comprehensibility for users.

The implementation of the flood detection system may present certain challenges. The integration and calibration of the sensors are essential for ensuring precise data collection. A reliable transmission of data from the sensors to the cloud platform requires a robust communication infrastructure. The system must prioritize the careful addressing of data security and privacy due to the collection and processing of sensitive information.

In summary, the development of a flood detection system using sensors, a cloud platform, and a user-friendly dashboard offers a promising solution to the challenges posed by frequent floods in low-lying areas. By enabling real-time flood detection, generating timely alerts, and providing critical information to users, the system has the potential to enhance preparedness, reduce damages, and save lives. Careful attention to technical considerations, stakeholder engagement, and ongoing maintenance will be crucial to realizing the full potential of this flood detection system.

7.0 Conclusion
In conclusion, the problem statement highlights the need for an improved flood detection system to address the recurring issue of floods in low-lying areas. Traditional methods have proven inadequate in terms of scope, accuracy, and timely detection, necessitating the development of a more reliable and efficient solution. This project aims to tackle this challenge by leveraging sensors, a cloud platform, and a dashboard to detect floods in real-time, issue alerts, and equip users with crucial information for minimizing the impact of floods.

Appendix A : Coding ESP32

#include <WiFi.h>
#include <PubSubClient.h>
#include <NewPing.h>

// Ultrasonic sensor configuration
#define TRIGGER_PIN D5
#define ECHO_PIN D6
#define MAX_DISTANCE 200

// Wi-Fi credentials
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

// MQTT broker configuration
const char* mqtt_broker = "a5da1b92468e4cd6b6dd31c7909a5cc6.s2.eu.hivemq.cloud";
const int mqtt_port = 8883;
mqtt_topic = "floodsentry";
const char* mqtt_username = "admin";
const char* mqtt_password = "Admin1234";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  mqttClient.setServer(mqtt_broker, mqtt_port);
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println("Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void loop() {
  delay(2000);

  unsigned int distance = sonar.ping_cm();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  if (mqttClient.connected()) {
    String payload = String(distance);
    mqttClient.publish(mqtt_topic + "/ultrasonic", payload.c_str());
  } else {
    Serial.println("MQTT connection lost. Reconnecting...");
    if (mqttClient.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
    }
  }
}


Appendix B: Coding server

#!/usr/bin/env python
#Import modules
import paho.mqtt.client as paho
from paho import mqtt
from flask import Flask, render_template, jsonify, request
from influxdb import InfluxDBClient
import threading
import psycopg2
import configparser

data_collection = True
table_name = ['ultrasonic', 'waterlevel']

config = configparser.ConfigParser()                                 
config.read('config.ini')                                            

#Hive MQTT Broker Configuration
HIVEMQTT_BROKER = config.get('MQTT Broker', 'HIVEMQTT_BROKER')
HIVEMQTT_PORT = config.getint('MQTT Broker', 'HIVEMQTT_PORT')
HIVEMQTT_TOPIC = config.get('MQTT Broker', 'HIVEMQTT_TOPIC')
HIVEMQTT_USERNAME = config.get('MQTT Broker', 'HIVEMQTT_USERNAME')
HIVEMQTT_PASSWORD = config.get('MQTT Broker', 'HIVEMQTT_PASSWORD')

#InfluxDB Configuration
INFLUXDB_HOST = config.get('InfluxDB', 'INFLUXDB_HOST')
INFLUXDB_PORT = config.getint('InfluxDB', 'INFLUXDB_PORT')
INFLUXDB_DATABASE = config.get('InfluxDB', 'INFLUXDB_DATABASE')

#PostgreSQL Configuration
POSTGRESQL_HOST = config.get('PostgreSQL', 'POSTGRESQL_HOST')
POSTGRESQL_PORT = config.getint('PostgreSQL', 'POSTGRESQL_PORT')
POSTGRESQL_DATABASE = config.get('PostgreSQL', 'POSTGRESQL_DATABASE')
POSTGRESQL_USER = config.get('PostgreSQL', 'POSTGRESQL_USER')
POSTGRESQL_PASSWORD = config.get('PostgreSQL', 'POSTGRESQL_PASSWORD')

app = Flask(__name__)                                                 

@app.route("/")                                                        
#Handle requests to the root URL
def index():  
    postgresql_client = psycopg2.connect(                              
        host=POSTGRESQL_HOST,
        port=POSTGRESQL_PORT,
        database=POSTGRESQL_DATABASE,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD
    )
    cursor = postgresql_client.cursor()

    # Fetch data from the PostgreSQL tables
    cursor.execute("SELECT * FROM ultrasonic")
    ultrasonic_rows = cursor.fetchall()
    cursor.execute("SELECT * FROM waterlevel")
    waterlevel_rows = cursor.fetchall()

    # Render the data in the HTML template
    return render_template('index.html', ultrasonic_rows=ultrasonic_rows, waterlevel_rows=waterlevel_rows)      

@app.route('/change_data_collection', methods=['POST'])
def change_data_collection():
    global data_collection
    data_collection = not data_collection  # Toggle the value of data_collection
    print(f'Data collection: {data_collection}')
    return jsonify(data_collection=data_collection)

#Route to handle the measurement deletion
@app.route('/delete_measurement', methods=['POST'])
def delete_measurement():
    for i in range(len(table_name)):
        influxdb_client.query(f'DROP MEASUREMENT {table_name[i]}')
    print('Data cleared')
    return 'Data cleared'

#Callback function when mqtt connected
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")

#Callback function when mqtt subscribed
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("MQTT Topic Subscribed: " + str(mid))

#Callback function when mqtt message received
def on_message(client, userdata, msg):
    if data_collection == True:
        print("Data collection started")
        print("Topic: " + msg.topic + " " + str(msg.payload))
        influxdb(msg.topic, msg.payload, measurement="ultrasonic")
        waterlevel = calc_waterlevel(msg.payload)
        influxdb(msg.topic, waterlevel, measurement="waterlevel")
    else:
        #hivemqtt_client.disconnect()
        print("Data collection stopped")
    for i in range(len(table_name)):
        postgresql(influxdb_client, table_name[i])
    
#Initialize Hive MQTT client
def hivemqtt():
    global hivemqtt_client
    hivemqtt_client = paho.Client(                                      
        client_id="",                                                   
        userdata=None,                                                  
        protocol=paho.MQTTv5                                            
    )
    hivemqtt_client.on_connect = on_connect                             
    hivemqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)   
    hivemqtt_client.username_pw_set(HIVEMQTT_USERNAME, HIVEMQTT_PASSWORD)       
    hivemqtt_client.connect(HIVEMQTT_BROKER, HIVEMQTT_PORT)                     
    hivemqtt_client.on_subscribe = on_subscribe                         
    hivemqtt_client.on_message = on_message                             

    hivemqtt_client.subscribe(HIVEMQTT_TOPIC + "/#", qos=1)            
    hivemqtt_client.publish(HIVEMQTT_TOPIC + "/ultrasonic",            
                        payload="0", 
                        qos=1
    ) 
    hivemqtt_client.loop_forever()                                    

#Save MQTT data to InfluxDB
def influxdb(topic, payload, measurement):
    try:
        global influxdb_client
        influxdb_client = InfluxDBClient(                              
            host=INFLUXDB_HOST, 
            port=INFLUXDB_PORT
        )
        influxdb_client.create_database(INFLUXDB_DATABASE)             
        influxdb_client.switch_database(INFLUXDB_DATABASE)              
        data_point = {                                                 
            "measurement": measurement,
            "tags": {
                "topic": topic
            },
            "fields": {
                "value": float(payload)
            }
        }
        influxdb_client.write_points([data_point])
    
        print("Successfully stored in InfluxDB:", data_point)
    except Exception as e:
        print("Error storing data in InfluxDB:", str(e))

#Calculate water level
def calc_waterlevel(payload):
    waterlevel = 100-float(payload)
    return waterlevel

#Save InfluxDB data into PostgreSQL
def postgresql(influxdb_client, table_name):
    try:
        postgresql_client = psycopg2.connect(                        
        host=POSTGRESQL_HOST,
        port=POSTGRESQL_PORT,
        database=POSTGRESQL_DATABASE,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD
        )
        query = f'SELECT * FROM {table_name}'                          
        result = influxdb_client.query(query)
        cursor = postgresql_client.cursor()                            
        cursor.execute(f'DROP TABLE IF EXISTS {table_name};')          
        cursor.execute(f'''CREATE TABLE {table_name} (                  
                                 id serial PRIMARY KEY,
                                 time varchar NOT NULL,
                                 topic varchar NOT NULL,
                                 value float NOT NULL
        )''')                                                           
        for point in result.get_points():                            
            time = point['time']                                         
            topic = point['topic']                                       
            value = point['value']                                      

            insert_query = f'''INSERT INTO {table_name} (time, topic, value) VALUES (%s, %s, %s)'''    
            cursor.execute(insert_query, (time, topic, value))          

        postgresql_client.commit()                                      
        cursor.close()                                                  
        postgresql_client.close()                                       

        print(f"Successfully stored {table_name} in PostgreSQL")
    except Exception as e:
        print(f"Error storing {table_name} in PostgreSQL:", str(e))

if __name__ == '__main__':                                              
    hivemqtt = threading.Thread(target=hivemqtt)                        
    hivemqtt.start()                                                    
    app.run()  
