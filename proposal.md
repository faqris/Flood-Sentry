# Flood Sentry
### Software Engineering (SEEL4213)
#### Group: Rampaging Rhinos

<br> 

#### Table of contents

<br>

[1.0 Problem Statement](#10-problem-statement)

[2.0 System Architecture](#20-system-architecture)

[3.0 Sensor](#30-sensor)
> [3.1 Nodemcu ESP32](#31-nodemcu-esp32)
>
> [3.2 Ultrasonic HC-SR04](#32-ultrasonic-hc-sr04)
> 
> [3.3 MQTT](#33-mqtt)

[4.0 Cloud Platform](#40-cloud-platform)
> [4.1 PythonAnywhere](#41-pythonanywhere)
>
> [4.2 Demo Video](#42-demo-video)

[5.0 Dashboard](#50-dashboard)
> [5.1 Grafana](#51-grafana)
>
> [5.2 User Interface](#52-user-interface)

<br>

## 1.0 Problem Statement


## 2.0 System Architecture

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![](./img/system_arch.png)

The system architecture consists of a ultrasonic HC-SR04 sensor that sends data to a microcontroller, which is NodeMCU ESP32. It connects to a Mosquitto MQTT broker and send the data via wifi. A Python Flask application run on a server hosted on PythonAnywhere subscribes to the MQTT broker, receives the data and stores it to an InfluxDB database. Grafana reads the data from InfluxDB database and visualize it in real-time dashboards. The dashboard is accessible to user via a public URL that is hosted on the PythonAnywhere cloud platform.

## 3.0 Sensor 

#### 3.1 Nodemcu ESP32

The NodeMCU ESP32 is a powerful microcontroller that is ideal for your flood detection system. It features built-in WiFi and Bluetooth capabilities, making it easy to connect to the cloud platform and communicate with other devices. With its low power consumption and small form factor, the NodeMCU ESP32 is perfect for use in remote areas where power may be limited.
To detect floods, you can use various sensors such as water level sensors, pressure sensors, or flow sensors. These sensors can be connected to the NodeMCU ESP32, which will collect the sensor data and send it to the cloud platform for further processing and analysis. The NodeMCU ESP32 can also be programmed to perform real-time analysis on the data collected by the sensors, allowing for immediate detection and alert generation.
In addition to flood detection, the NodeMCU ESP32 can be used for other applications, such as monitoring weather conditions and tracking environmental changes. Its versatility and ease of use make it an excellent choice for any project that requires reliable and efficient data collection and analysis.

#### 3.2 Ultrasonic HC-SR04

In your flood detection system, the HC-SR04 sensor can be used as a water level sensor to measure the distance between the sensor and the water surface. By measuring the distance, you can determine the water level in real-time.
To use the HC-SR04 sensor for water level detection, you will need to connect it to your NodeMCU ESP32 microcontroller. You can do this by connecting the VCC and GND pins of the sensor to the corresponding pins on the NodeMCU ESP32. You will also need to connect the Echo and Trig pins of the sensor to two available GPIO pins on the NodeMCU ESP32.
Once the sensor is connected, you can write code to collect data from the sensor and send it to the cloud platform for analysis. The NodeMCU ESP32 can be programmed to perform real-time analysis on the data collected by the sensor, allowing for immediate detection and alert generation.

#### 3.3 MQTT
MQTT (Message Queuing Telemetry Transport) is a lightweight, open-source messaging protocol that is ideal for use in IoT (Internet of Things) applications. In your flood detection system, MQTT can be used to establish a connection between your NodeMCU ESP32 microcontroller and the cloud platform.

## 4.0 Cloud Platform

#### 4.1 PythonAnywhere
PythonAnywhere allows users to write and run Python code in the cloud, which is particularly useful for IoT projects that require a persistent and reliable connection. Additionally, PythonAnywhere provides a range of pre-installed libraries and packages, including those for IoT-related tasks such as data processing and visualization. It also has support for many popular IoT hardware devices, making it easy to interface with sensors and other devices. Finally, PythonAnywhere offers a simple user interface making it easy to manage and deploy IoT applications. 

#### 4.2 Demo Video
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [<img src="https://i.ytimg.com/vi/kyg1rLgmdiE/maxresdefault.jpg" width="50%">](https://youtu.be/kyg1rLgmdiE "Click this to open video")

Porting flask app from stage 1 to PythonAnywhere 

## 5.0 Dashboard

#### 5.1 Grafana


#### 5.2 User Interface

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![](./img/dashboard.png)
