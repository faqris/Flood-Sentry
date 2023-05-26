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
