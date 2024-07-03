import tkinter as tk
from tkinter import ttk
import subprocess
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("USPSS PROFILE HUB JETSON")

        self.running_facial_recognition = False
        self.running_rfid_detection = False

        self.configure(bg="#ffffff")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), foreground="white", background="#2196f3", borderwidth=0, padx=20, pady=10)
        style.map('TButton', background=[('active', '#1976d2')])

        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.pack(padx=20, pady=20)

        self.start_facial_detection_btn = ttk.Button(button_frame, text="START FACIAL DETECTION", command=self.start_facial_detection, style='TButton')
        self.start_facial_detection_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.end_facial_detection_btn = ttk.Button(button_frame, text="END FACIAL DETECTION", command=self.end_facial_detection, state="disabled", style='TButton')
        self.end_facial_detection_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.start_rfid_detection_btn = ttk.Button(button_frame, text="START RFID DETECTION", command=self.start_rfid_detection, style='TButton')
        self.start_rfid_detection_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.end_rfid_detection_btn = ttk.Button(button_frame, text="END RFID DETECTION", command=self.end_rfid_detection, state="disabled", style='TButton')
        self.end_rfid_detection_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = (self.winfo_screenwidth() - width) // 2
        y_offset = (self.winfo_screenheight() - height) // 2
        self.geometry(f"500x300+{x_offset}+{y_offset}")

    def start_facial_detection(self):
        if not self.running_facial_recognition:
            self.running_facial_recognition = True
            self.start_facial_detection_btn.config(state="disabled")
            self.end_facial_detection_btn.config(state="normal")
            subprocess.Popen(["python3", "FACIAL_RECOGNITION.py"])

    def end_facial_detection(self):
        if self.running_facial_recognition:
            self.running_facial_recognition = False
            self.start_facial_detection_btn.config(state="normal")
            self.end_facial_detection_btn.config(state="disabled")
            os.system("pkill -f FACIAL_RECOGNITION.py")
            # Delete the facial detection log file
            if os.path.exists("CSV/FACE_LOG.csv"):
                os.remove("CSV/FACE_LOG.csv")

    def start_rfid_detection(self):
        if not self.running_rfid_detection:
            self.running_rfid_detection = True
            self.start_rfid_detection_btn.config(state="disabled")
            self.end_rfid_detection_btn.config(state="normal")
            password = "jetson\n"
            subprocess.Popen(["sudo", "-S", "./PEERMISSION.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=password.encode())
            subprocess.Popen(["python3", "RFID.py"])

    def end_rfid_detection(self):
        if self.running_rfid_detection:
            self.running_rfid_detection = False
            self.start_rfid_detection_btn.config(state="normal")
            self.end_rfid_detection_btn.config(state="disabled")
            os.system("pkill -f RFID.py")
	    # Delete the RFID log file
            if os.path.exists("CSV/ENTRY_EXIT.csv"):
                os.remove("CSV/ENTRY_EXIT.csv")

if __name__ == "__main__":
    app = Application()
    app.mainloop()

