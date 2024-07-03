import serial
import csv
import time

authorized_UID = "D3 B4 30 A8"  # Authorized UID
person_name = "Yuvraj Dutta"  # Person associated with authorized UID
log_file = "CSV/ENTRY_EXIT.csv"  # CSV file to store combined entry and exit log

# Dictionary to keep track of entry times for each UID
entry_times = {}
# Dictionary to keep track of entry rows for each UID
entry_rows = {}

# Open serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Adjust the serial port as per your Jetson Nano configuration

try:
    while True:
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write header if file is empty
            if file.tell() == 0:
                writer.writerow(["Person Name", "UID", "Authorized", "Entry Time", "Exit Time"])

            line = ser.readline().decode().strip()  # Read line from serial
            if line:  # If line is not empty
                uid = line.split(',')[0]  # Extract UID
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                authorized = "Yes" if uid == authorized_UID else "No"
                person = person_name if uid == authorized_UID else "Unknown"

                if uid in entry_rows:
                    # UID has entered before
                    entry_row = entry_rows.pop(uid)  # Retrieve entry row
                    entry_row[4] = timestamp  # Update exit time
                    writer.writerow(entry_row)  # Write updated entry row
                    print("Exit logged:", person, uid, timestamp)
                else:
                    # UID is entering for the first time
                    entry_times[uid] = timestamp  # Record entry time for UID
                    entry_rows[uid] = [person, uid, authorized, timestamp, ""]  # Store entry row
                    print("Entry logged:", person, uid, timestamp)

finally:
    ser.close()  # Close serial connection

