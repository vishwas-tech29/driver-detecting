# Driver Monitoring System

## Overview
The **Driver Monitoring System** is a Python-based application designed to monitor and analyze driver behavior in real-time. It uses computer vision and machine learning techniques to detect various driver activities, such as sleeping, being active, phone usage, yawning, and head pose. The system also incorporates alerts for potential hazards and behavior detection, enhancing driver safety.

## Features
- **Eye Blink & Drowsiness Detection**: Monitors the driver's eye state to detect signs of drowsiness.
- **Phone Usage Detection**: Detects if the driver is using their phone, with alerts triggered if it’s the case.
- **Yawning Detection**: Detects yawning behavior, indicating potential sleepiness.
- **Head Pose Estimation**: Analyzes the driver’s head position to understand if they are looking at the road or distracted.
- **Face Detection**: Recognizes the driver and can alert when the driver is not paying attention.
- **Alert System**: Triggers an alert when any suspicious or unsafe behavior is detected.
- **Real-Time Monitoring**: Provides a live feed of the driver's behavior, along with alerts.

## Technologies Used
- **Python 3.10**: Main programming language.
- **OpenCV**: For image processing and computer vision tasks.
- **MediaPipe**: For face detection and pose estimation.
- **TensorFlow Lite**: For phone usage detection.
- **YOLOv8 (optional)**: For object detection (if used for additional tasks).
- **CMake**: For compiling and building dependencies.

## Installation
### Prerequisites
- Install Python 3.10 and necessary libraries.

### Step 1: Clone the repository

git clone https://github.com/yourusername/driver-monitoring-system.git
cd driver-monitoring-system

Step 2: Install dependencies
pip install -r requirements.txt
Step 3: Run the system
To start the monitoring system, use the following command:

python driver_monitoring_system.py
Project Structure

driver-monitoring-system/
│
├── driver_monitoring_system.py    # Main application file
├── README.md                     # Project overview and instructions
├── requirements.txt              # Python dependencies
├── models/                       # Pre-trained models for detection
│   ├── face_detection.tflite
│   ├── phone_detection.tflite
│   └── ...
├── logs/                         # Log files for alerts and driver activity
│   ├── activity_log.txt
│   └── ...
└── utils/                        # Utility scripts and helper functions
    ├── detection.py              # Contains code for detection algorithms
    ├── alert.py                  # Code for triggering alerts
    └── ...
Usage
The system uses a webcam to track the driver's behavior.

It will alert you with a sound when it detects dangerous behaviors, such as sleeping or phone usage.

You can adjust the alert thresholds and detection sensitivity in the config.py file.

Contributing
If you’d like to contribute to this project, feel free to fork it and create a pull request. Contributions are welcome, especially for improving detection algorithms or adding new features.

Issues
Please report any bugs or issues on the GitHub Issues page.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
OpenCV for computer vision tasks.

MediaPipe for pose and face detection.

TensorFlow Lite for phone detection.


Feel free to modify the content as needed, especially the project structure and dependencies! Let me know if you need any specific changes or additions.
