# Universal Student Profiling System

## Overview
The Universal Student Profiling System is designed to enhance campus safety by integrating advanced technologies such as one-shot facial recognition, AI-based activity detection and RFID. This project leverages various hardware and software components to create a comprehensive profiling system for students.

## Table of Contents
- [Objectives](#objectives)
- [System Architecture](#system-architecture)
- [Hardware Setup](#hardware-setup)
- [Software Components](#software-components)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Objectives
1. Develop a centralized database for student information.
2. Implement secure access control with RFID cards.
3. Integrate high-resolution IP cameras with facial recognition.
4. Use AI for real-time activity detection.
5. Streamline meal management processes.

## System Architecture
The system architecture consists of three main components:
1. **RFID System**: For secure access control.
2. **Facial Recognition System**: For identifying students using high-resolution cameras.
3. **Activity Detection System**: For monitoring and detecting student activities using AI.

### Hardware Setup
The hardware components used in this project include:
- **RFID Reader**: To read RFID cards for access control.
- **IP Cameras**: For capturing high-resolution images for facial recognition.
- **NVIDIA Jetson Nano**: For processing facial recognition and activity detection algorithms.
- **Arduino**: For controlling the RFID reader and interfacing with other components.

### Software Components
The software components include:
- **RFID_VAL.ino**: Arduino code for reading RFID cards.
- **FACIAL_RECOGNITION.py**: Python script for facial recognition using the Jetson Nano.
- **RFID.py**: Python script for handling RFID card data on the Jetson Nano.
- **USPSS_PROFILE_HUB_JETSON.py**: Main script for managing student profiles and integrating facial recognition and RFID data.
- **ACTIVITY_DETECTION/NOTEBOOK.ipynb**: Jupyter notebook for developing and testing activity detection algorithms.

## Installation
### Prerequisites
- Python 3.x
- Arduino IDE
- JetPack SDK for Jetson Nano
- Jupyter Notebook
- Required Python libraries: OpenCV, dlib, numpy, etc.

### Steps
1. **Clone the Repository**:
   - Set up SSH keys for secure access to GitHub:
     1. **Generate SSH Key**:
        ```bash
        ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
        ```
        Follow the prompts to save the key (default location is usually fine).
     2. **Add SSH Key to GitHub**:
        - Copy the SSH key to your clipboard:
          ```bash
          cat ~/.ssh/id_rsa.pub
          ```
        - Go to GitHub, navigate to **Settings** > **SSH and GPG keys**, and click **New SSH key**. Paste the key and save.
     3. **Clone the repository using SSH**:
        ```bash
        git clone git@github.com:your-username/universal-student-profiling-system.git
        cd universal-student-profiling-system
        ```

2. **Setup RFID System**:
   - Open `ARDUINO_SIDE/RFID_VAL.ino` in the Arduino IDE.
   - Upload the code to the Arduino board.
   - Connect the RFID reader to the Arduino as per the circuit diagram provided in the `hardware` folder.

3. **Setup Facial Recognition System**:
   - Ensure the Jetson Nano is properly configured with JetPack SDK.
   - Install required Python libraries:
     ```bash
     pip install opencv-python dlib numpy
     ```
   - Run `JETSON_SIDE/FACIAL_RECOGNITION.py` to test the facial recognition system.

4. **Integrate RFID and Facial Recognition**:
   - Run `JETSON_SIDE/USPSS_PROFILE_HUB_JETSON.py` to start the main profiling system.
   - The system will read data from the RFID reader and use the camera to perform facial recognition.

5. **Setup Activity Detection System**:
   - Open `PC_SIDE/ACTIVITY_DETECTION/NOTEBOOK.ipynb` in Jupyter Notebook.
   - Follow the steps in the notebook to train and test activity detection models.

## Usage
### Running the System
1. Start the Arduino RFID reader.
2. Run the main profiling system:
   ```bash
   python JETSON_SIDE/USPSS_PROFILE_HUB_JETSON.py
