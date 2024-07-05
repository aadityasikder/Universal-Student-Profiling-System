# Universal Student Profiling System

## Overview
The Universal Student Profiling System is an advanced campus security and management solution developed by a team of B.Tech 6th Semester Electronics and Communication Engineering students. It integrates facial recognition, RFID-based access control, and AI-driven activity detection to enhance campus safety and streamline operations.

## Features
- One-shot facial recognition for student identification
- RFID card integration for access control and verification
- Abnormal activity detection using LSTM+CNN models
- Real-time video streaming and monitoring
- User-friendly GUI for both Jetson Nano and remote PC control

## Technologies Used
- Python
- OpenCV
- TensorFlow / Keras
- Face Recognition library
- MFRC522 RFID library
- Arduino UNO
- Tkinter for GUI
- Paramiko for SSH communication

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/aadityasikder/Universal-Student-Profiling-System.git
   ```

2. Set up the Jetson Nano and RFID reader according to the hardware specifications in the documentation.

## Usage

1. Start the Jetson Nano GUI:
   ```
   python USPSS_PROFILE_HUB_JETSON.py   or  run the executable USPSS_PROFILE_HUB_JETSON
   ```

2. On a remote PC, start the control GUI:
   ```
   python USPSS_PROFILE_HUB_PC.py
   ```

3. Follow the on-screen instructions to connect to the Jetson Nano and control the system.

## Project Structure

- `Universal-Student-Profiling-System/`: Contains the source code for facial recognition, RFID detection, activity detection, and GUI.
- `JETSON_SIDE/`: Stores the code, executable, photos that needs to be identified, One-shot Machine Learning model from the Jetson Nano Side
- `JETSON_SIDE/PHOTOS`: Includes sample data and photos for facial recognition.
- 'ARDUINO_SIDE/': Contains code that is loaded in arduino to implement the RFID
- 'PC_SIDE/': Contains executable GUI program to control facial entry and RFID entry system that will be stored in  a file as csv
- `Documentation/`: Contains project documentation.

## Contributors
- [Aaditya Sikder](https://github.com/aadityasikder)
- [Tridib Jyoti Das](https://github.com/wheezydeeeb)
- [Yuvraj Dutta](https://github.com/YDT007))

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Usage
### Running the System
1. Start the Arduino RFID reader.
2. Run the main profiling system:
   ```bash
   python JETSON_SIDE/USPSS_PROFILE_HUB_JETSON.py
