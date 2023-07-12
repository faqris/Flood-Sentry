#!/usr/bin/env python
# Import modules
import paho.mqtt.client as paho
from paho import mqtt
from flask import Flask, render_template, jsonify, request
from influxdb import InfluxDBClient
import threading
import psycopg2
import configparser

data_collection = True
table_name = ['ultrasonic', 'waterlevel']

config = configparser.ConfigParser()                                  # Create a ConfigParser instance
config.read('config.ini')                                             # Read the configuration file

# Hive MQTT Broker Configuration
HIVEMQTT_BROKER = config.get('MQTT Broker', 'HIVEMQTT_BROKER')
HIVEMQTT_PORT = config.getint('MQTT Broker', 'HIVEMQTT_PORT')
HIVEMQTT_TOPIC = config.get('MQTT Broker', 'HIVEMQTT_TOPIC')
HIVEMQTT_USERNAME = config.get('MQTT Broker', 'HIVEMQTT_USERNAME')
HIVEMQTT_PASSWORD = config.get('MQTT Broker', 'HIVEMQTT_PASSWORD')

# InfluxDB Configuration
INFLUXDB_HOST = config.get('InfluxDB', 'INFLUXDB_HOST')
INFLUXDB_PORT = config.getint('InfluxDB', 'INFLUXDB_PORT')
INFLUXDB_DATABASE = config.get('InfluxDB', 'INFLUXDB_DATABASE')

# PostgreSQL Configuration
POSTGRESQL_HOST = config.get('PostgreSQL', 'POSTGRESQL_HOST')
POSTGRESQL_PORT = config.getint('PostgreSQL', 'POSTGRESQL_PORT')
POSTGRESQL_DATABASE = config.get('PostgreSQL', 'POSTGRESQL_DATABASE')
POSTGRESQL_USER = config.get('PostgreSQL', 'POSTGRESQL_USER')
POSTGRESQL_PASSWORD = config.get('PostgreSQL', 'POSTGRESQL_PASSWORD')

app = Flask(__name__)                                                   # Initialize Flask

@app.route("/")                                                         # Define a route for the root URL
# Handle requests to the root URL
def index():  
    postgresql_client = psycopg2.connect(                               # Connect to PostgreSQL
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

# Route to handle the measurement deletion
@app.route('/delete_measurement', methods=['POST'])
def delete_measurement():
    for i in range(len(table_name)):
        influxdb_client.query(f'DROP MEASUREMENT {table_name[i]}')
    print('Data cleared')
    return 'Data cleared'

# Callback function when mqtt connected
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")

# Callback function when mqtt subscribed
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("MQTT Topic Subscribed: " + str(mid))

# Callback function when mqtt message received
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
    
# Initialize Hive MQTT client
def hivemqtt():
    global hivemqtt_client
    hivemqtt_client = paho.Client(                                      # Initialize MQTT client
        client_id="",                                                   # Unique client identifier (empty string for automatic generation)
        userdata=None,                                                  # User-defined data passed to callbacks
        protocol=paho.MQTTv5                                            # Use MQTT version 5
    )
    hivemqtt_client.on_connect = on_connect                             # Set the on_connect callback function
    hivemqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)   # Set TLS version for secure connection
    hivemqtt_client.username_pw_set(HIVEMQTT_USERNAME, HIVEMQTT_PASSWORD)       # Set MQTT username and password
    hivemqtt_client.connect(HIVEMQTT_BROKER, HIVEMQTT_PORT)                     # Connect to the MQTT broker
    hivemqtt_client.on_subscribe = on_subscribe                         # Set the on_subscribe callback function
    hivemqtt_client.on_message = on_message                             # Set the on_message callback function

    hivemqtt_client.subscribe(HIVEMQTT_TOPIC + "/#", qos=1)             # Subscribe to a topic pattern (wildcard) with QoS level 1             
    hivemqtt_client.publish(HIVEMQTT_TOPIC + "/ultrasonic",             # Publish a message to a ultrasonic topic with QoS level 1
                        payload="0", 
                        qos=1
    ) 
    hivemqtt_client.loop_forever()                                      # Enter the network loop and keep the client running indefinitely

# Save MQTT data to InfluxDB
def influxdb(topic, payload, measurement):
    try:
        global influxdb_client
        influxdb_client = InfluxDBClient(                               # Connect to InfluxDB
            host=INFLUXDB_HOST, 
            port=INFLUXDB_PORT
        )
        influxdb_client.create_database(INFLUXDB_DATABASE)              # Create a new database in InfluxDB 
        influxdb_client.switch_database(INFLUXDB_DATABASE)              # Switch to the specified database in InfluxDB
        data_point = {                                                  # Write data to InfluxDB
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

# Calculate water level
def calc_waterlevel(payload):
    waterlevel = 100-float(payload)
    return waterlevel

# Save InfluxDB data into PostgreSQL
def postgresql(influxdb_client, table_name):
    try:
        postgresql_client = psycopg2.connect(                           # Connect to PostgreSQL
        host=POSTGRESQL_HOST,
        port=POSTGRESQL_PORT,
        database=POSTGRESQL_DATABASE,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD
        )
        query = f'SELECT * FROM {table_name}'                           # Query data from PostgreSQL
        result = influxdb_client.query(query)
        cursor = postgresql_client.cursor()                             # Create a cursor
        cursor.execute(f'DROP TABLE IF EXISTS {table_name};')           # Drop the table if it exists
        cursor.execute(f'''CREATE TABLE {table_name} (                  
                                 id serial PRIMARY KEY,
                                 time varchar NOT NULL,
                                 topic varchar NOT NULL,
                                 value float NOT NULL
        )''')                                                           # Create a new table with specified columns
        for point in result.get_points():                            
            time = point['time']                                        # Extract the 'time' value from the InfluxDB 
            topic = point['topic']                                      # Extract the 'topic' value from the InfluxDB 
            value = point['value']                                      # Extract the 'value' value from the InfluxDB 

            insert_query = f'''INSERT INTO {table_name} (time, topic, value) VALUES (%s, %s, %s)'''    
            cursor.execute(insert_query, (time, topic, value))          # Insert data into table in PostgreSQL

        postgresql_client.commit()                                      # Commit the changes
        cursor.close()                                                  # Close the cursor
        postgresql_client.close()                                       # Close the connection

        print(f"Successfully stored {table_name} in PostgreSQL")
    except Exception as e:
        print(f"Error storing {table_name} in PostgreSQL:", str(e))

if __name__ == '__main__':                                              # Ensures that it is executed only when the script is run directly (not imported as a module)
    hivemqtt = threading.Thread(target=hivemqtt)                        # Create a new thread for hivemqtt
    hivemqtt.start()                                                    # Start the thread execution
    app.run()                                                           # Start the Flask application
