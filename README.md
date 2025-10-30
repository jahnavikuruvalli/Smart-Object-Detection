🧠 Hybrid Object Detection System using Camera and LDR
A smart, low-cost object detection system that combines computer vision (via camera) and light intensity sensing (via LDR + Arduino). The project detects the presence of objects using both optical input from a webcam and real-time brightness data from the LDR sensor, ensuring reliable detection even under varying lighting conditions.

⚙️ Features
Dual-mode detection (Camera + LDR sensor)
Real-time data processing using Python and Arduino
Automatic LED indicator for object detection
Easily extendable for IoT or machine learning integration

🧩 Hardware Requirements
Arduino Uno
LDR sensor
10kΩ resistor
220Ω resistor
LED
USB cable
Jumper wires

💻 Software Requirements
Arduino IDE
Python 3
OpenCV library
PySerial library
Homebrew (for managing dependencies on macOS)

🔌 Circuit Overview
LDR connected to A0 on Arduino
LED connected to Pin 13
Common GND between components

🚀 How It Works
The Arduino reads the light intensity from the LDR.
The Python script activates the MacBook camera to capture frames.
If the LDR or camera detects a significant object or shadow, an alert is triggered.
The LED glows when an object is detected.

🧠 Applications
Smart home automation
Security surveillance
Robotic vision systems
Object tracking under variable lighting

🧑‍💻 Developed By

Jahnavi Karanam & Ahana Banerjee
ECE  | JNTU College of Engineering, Hyderabad
