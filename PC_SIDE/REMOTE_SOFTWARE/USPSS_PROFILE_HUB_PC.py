import csv
import cv2
import numpy as np
import socket
import pickle
import struct
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import paramiko
from tkintertable import TableCanvas, TableModel

class SSHClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("SSH Client")
        
        self.label_host = tk.Label(master, text="Host:")
        self.label_host.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_host = tk.Entry(master)
        self.entry_host.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_username = tk.Label(master, text="Username:")
        self.label_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=1, column=1, padx=10, pady=5)
        
        self.label_password = tk.Label(master, text="Password:")
        self.label_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5)
        
        self.btn_connect = tk.Button(master, text="Connect", command=self.connect_ssh)
        self.btn_connect.grid(row=3, column=0, padx=10, pady=5)

        self.btn_disconnect = tk.Button(master, text="Disconnect", command=self.disconnect_ssh, state=tk.DISABLED)
        self.btn_disconnect.grid(row=3, column=1, padx=10, pady=5)

        self.btn_facial_recognition = tk.Button(master, text="Start Facial Recognition", command=self.start_facial_recognition, state=tk.DISABLED)
        self.btn_facial_recognition.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.btn_rfid_authentication = tk.Button(master, text="RFID Authentication", command=self.rfid_authentication, state=tk.DISABLED)
        self.btn_rfid_authentication.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.btn_face_log = tk.Button(master, text="Facial Recognition Log", command=self.display_face_log, state=tk.DISABLED)
        self.btn_face_log.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.ssh_client = None
        self.connection = None
        self.streaming_thread = None
        self.streaming_active = False

        # Handle window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_ssh(self):
        host = self.entry_host.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not host or not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=host, username=username, password=password)
            messagebox.showinfo("Success", "Connected to {} successfully!".format(host))
            self.btn_connect.config(state=tk.DISABLED)
            self.btn_disconnect.config(state=tk.NORMAL)
            self.btn_facial_recognition.config(state=tk.NORMAL)
            self.btn_rfid_authentication.config(state=tk.NORMAL)
            self.btn_face_log.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", "Failed to connect: {}".format(str(e)))

    def disconnect_ssh(self):
        if self.connection:
            self.connection.close()
        if self.ssh_client:
            self.ssh_client.close()
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)
        self.btn_facial_recognition.config(state=tk.DISABLED)
        self.btn_rfid_authentication.config(state=tk.DISABLED)
        self.btn_face_log.config(state=tk.DISABLED)

    def start_facial_recognition(self):
        if not self.ssh_client:
            messagebox.showerror("Error", "Please connect via SSH first")
            return

        self.btn_facial_recognition.config(state=tk.DISABLED)
        self.streaming_thread = threading.Thread(target=self.display_stream)
        self.streaming_thread.start()

    def stop_stream(self):
        self.streaming_active = False
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.NORMAL)
        self.btn_facial_recognition.config(state=tk.NORMAL)
        self.btn_rfid_authentication.config(state=tk.NORMAL)
        self.btn_face_log.config(state=tk.NORMAL)

    def receive_frames(self):
        host = self.entry_host.get()
        port = 2947

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            while len(data) < payload_size:
                packet = self.connection.recv(4*1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.connection.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            yield frame

    def display_stream(self):
        self.streaming_active = True
        cv2.namedWindow("Facial Recognition Stream", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Facial Recognition Stream", 800, 600)

        for frame in self.receive_frames():
            if not self.streaming_active:
                break
            cv2.imshow("Facial Recognition Stream", frame)
            key = cv2.waitKey(1) & 0xFF
            # Listen for 'q' key press specifically in the OpenCV window
            if key == ord('q'):
                self.stop_stream()

        cv2.destroyAllWindows()

    def rfid_authentication(self):
        if not self.ssh_client:
            messagebox.showerror("Error", "Please connect via SSH first")
            return

        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_client.exec_command("cat USPSS/MASTER/CSV/ENTRY_EXIT.csv")
            csv_content = ssh_stdout.read().decode('utf-8')
            self.show_csv_viewer(csv_content)
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch CSV file: {}".format(str(e)))

    def display_face_log(self):
        if not self.ssh_client:
            messagebox.showerror("Error", "Please connect via SSH first")
            return

        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_client.exec_command("cat USPSS/MASTER/CSV/FACE_LOG.csv")
            csv_content = ssh_stdout.read().decode('utf-8')
            self.show_csv_viewer(csv_content)
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch CSV file: {}".format(str(e)))

    def show_csv_viewer(self, csv_content):
        csv_viewer_window = tk.Toplevel(self.master)
        csv_viewer_window.title("CSV Viewer")
        
        table = ttk.Treeview(csv_viewer_window)
        table.pack(expand=True, fill=tk.BOTH)

        csv_reader = csv.reader(csv_content.splitlines())
        header = next(csv_reader)
        table["columns"] = header
        table.heading("#0", text="Index")
        for col in header:
            table.heading(col, text=col)
        for i, row in enumerate(csv_reader):
            table.insert("", "end", text=i, values=row)

    def on_closing(self):
        if self.streaming_thread:
            self.stop_stream()
            self.streaming_thread.join()
        self.disconnect_ssh()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientGUI(root)
    root.mainloop()
