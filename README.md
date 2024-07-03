# Universal-Student-Profiling-System

Universal Student Profiling System
Overview
The Universal Student Profiling System is an advanced campus security and management solution developed by a team of B.Tech 6th Semester Electronics and Communication Engineering students. It integrates facial recognition, RFID-based access control, and AI-driven activity detection to enhance campus safety and streamline operations.
Features

One-shot facial recognition for student identification
RFID card integration for access control and verification
Abnormal activity detection using LSTM+CNN models
Real-time video streaming and monitoring
User-friendly GUI for both Jetson Nano and remote PC control

Technologies Used

Python
OpenCV
TensorFlow / Keras
Face Recognition library
MFRC522 RFID library
Tkinter for GUI
Paramiko for SSH communication

Installation

Clone the repository:
Copygit clone https://github.com/your-username/Universal-Student-Profiling-System.git

Install the required dependencies:
Copypip install -r requirements.txt

Set up the Jetson Nano and RFID reader according to the hardware specifications in the documentation.

Usage

Start the Jetson Nano GUI:
Copypython src/gui/jetson_gui.py

On a remote PC, start the control GUI:
Copypython src/gui/pc_gui.py

Follow the on-screen instructions to connect to the Jetson Nano and control the system.

Project Structure

src/: Contains the source code for facial recognition, RFID detection, activity detection, and GUI.
models/: Stores the trained machine learning models.
data/: Includes sample data and photos for facial recognition.
docs/: Contains project documentation.

Contributors

Gourab Chowdhury (121EC0268)
Yuvraj Dutta (121EC0272)
Aaditya Sikder (121EC0303)
Tridib Jyoti Das (121EC0899)

License
This project is licensed under the MIT License - see the LICENSE file for details.
