import cv2
import numpy as np
import socket
import pickle
import struct
import face_recognition
import csv
from datetime import datetime
import os
import threading

# Function to load images from a folder path and extract facial encodings
def load_images_from_folder(folder_path):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

    return known_face_encodings, known_face_names

# Function to append data to CSV file
def append_to_csv(name, entry_time):
    with open('CSV/FACE_LOG.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, entry_time])

# Function to handle client connections
def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")

    try:
        while True:
            # Receive data from the client (if any)
            try:
                data = client_socket.recv(1024)
            except ConnectionResetError:
                print(f"Client {addr} disconnected.")
                break

            # Check if client wants to disconnect
            if data == b'disconnect':
                print(f"Client {addr} requested disconnect.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()

# Path to the folder containing images of known faces
folder_path = "PHOTOS/"

# Load images from the folder and extract facial encodings
known_face_encodings, known_face_names = load_images_from_folder(folder_path)

# Initialize set to keep track of logged names
logged_names = set()

# Set threshold distance to consider a face as unknown
threshold_distance = 0.4  # You can adjust this value as needed

print("Streaming server started...")

# Socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.31.146', 2947))  # Binding to all interfaces
server_socket.listen(5)  # Listening for connections

# Function to send frames to clients
def send_frames_to_clients():
    video_capture = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_location, face_encoding in zip(face_locations, face_encodings):
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] < threshold_distance:
                    name = known_face_names[best_match_index]

                    if name not in logged_names:
                        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        append_to_csv(name, entry_time)
                        logged_names.add(name)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Serialize the frame
            data = pickle.dumps(frame)

            # Pack the message size and data together
            message_size = struct.pack("Q", len(data))
            
            # Send frame to all connected clients
            for client_socket, _ in clients:
                try:
                    client_socket.sendall(message_size + data)
                except Exception as e:
                    print(f"Error sending frame to client: {e}")
                    clients.remove((client_socket, _))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        video_capture.release()

# Start sending frames to clients in a separate thread
frame_sender_thread = threading.Thread(target=send_frames_to_clients)
frame_sender_thread.start()

# Accept client connections and handle them in separate threads
clients = []  # List to keep track of connected clients
while True:
    client_socket, addr = server_socket.accept()
    clients.append((client_socket, addr))
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()

