# ESP32 Motion Detection System

A real-time motion detection system built with **ESP32** and **MPU-6050**.  
This project detects movement using 3-axis accelerometer data and sends mobile notifications through **IFTTT**. It also supports remote **arm/disarm control** using **Google Assistant** and **ThingSpeak**.

## Overview

This project was designed as an IoT-based motion alert system. The ESP32 continuously reads acceleration data from the MPU-6050 sensor and determines whether motion has occurred based on predefined thresholds on the X, Y, and Z axes.  

When the system is armed and motion is detected, the ESP32 triggers an IFTTT webhook to send a notification to the user's phone. The system state can be changed remotely through Google Assistant voice commands, which update a ThingSpeak channel that the ESP32 periodically checks.

A typical use case is bag theft detection: once the system is armed, any unexpected movement can trigger an alert.

## Features

- Real-time motion detection using **MPU-6050**
- 3-axis acceleration monitoring over **I2C**
- Remote arm/disarm control through **Google Assistant**
- Cloud-based state communication using **ThingSpeak**
- Mobile alert notifications using **IFTTT Webhooks**
- LED / NeoPixel status indication for armed and disarmed states

## Hardware Used

- ESP32 Feather board
- Adafruit MPU-6050 sensor board
- Onboard LED / NeoPixel
- STEMMA QT cable or I2C connection

## Software / Services Used

- MicroPython
- `adafruit_mpu6050` library
- ThingSpeak
- IFTTT
- Google Assistant

## System Workflow

1. The user gives a voice command through Google Assistant to activate or deactivate the motion sensor.
2. IFTTT sends the command to a ThingSpeak channel.
3. The ESP32 periodically reads the latest channel value from ThingSpeak.
4. If the system is armed, the ESP32 monitors acceleration values from the MPU-6050.
5. If motion exceeds the threshold on any axis, the ESP32 sends a webhook request to IFTTT.
6. IFTTT pushes a notification to the phone.
7. LED indicators show whether the system is armed or disarmed.

## Motion Detection Logic

The system reads acceleration values along the X, Y, and Z axes and compares them against predefined thresholds.  
Motion is detected when any of the following conditions is met:

- `|Accel X| > threshold_x`
- `|Accel Y| > threshold_y`
- `|Accel Z| > threshold_z`

Before use, the accelerometer is calibrated to reduce offset and improve accuracy.

## Project Structure

```text
ESP32_project/
│── motion_detector.py
│── README.md
│── config.py              # optional, for API keys / thresholds
│── utils.py               # optional helper functions
