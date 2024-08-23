import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
from datetime import datetime
import pygame

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")

        self.alarms = []
        self.alarm_thread = None
        self.is_alarm_active = False
        self.snooze_time = 5  # Default snooze time in minutes

        pygame.mixer.init()

        self.create_widgets()

    def create_widgets(self):
        # Time selection
        self.time_label = tk.Label(self.root, text="Set Alarm Time (HH:MM):")
        self.time_label.pack()

        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        # Tone selection
        self.tone_label = tk.Label(self.root, text="Select Alarm Tone:")
        self.tone_label.pack()

        self.tone_button = tk.Button(self.root, text="Choose Tone", command=self.select_tone)
        self.tone_button.pack()

        self.selected_tone = tk.Label(self.root, text="No tone selected")
        self.selected_tone.pack()

        # Snooze time selection
        self.snooze_label = tk.Label(self.root, text="Snooze Time (minutes):")
        self.snooze_label.pack()

        self.snooze_entry = tk.Entry(self.root)
        self.snooze_entry.insert(0, "5")
        self.snooze_entry.pack()

        # Set alarm button
        self.set_button = tk.Button(self.root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack()

        # Active alarm display
        self.active_alarm_label = tk.Label(self.root, text="No active alarms")
        self.active_alarm_label.pack()

    def select_tone(self):
        self.alarm_tone = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if self.alarm_tone:
            self.selected_tone.config(text=self.alarm_tone)

    def set_alarm(self):
        alarm_time = self.time_entry.get()
        try:
            # Validate time format
            valid_time = datetime.strptime(alarm_time, "%H:%M")
            self.snooze_time = int(self.snooze_entry.get())

            alarm = {
                "time": alarm_time,
                "tone": self.alarm_tone,
                "snooze_time": self.snooze_time
            }

            self.alarms.append(alarm)
            self.active_alarm_label.config(text=f"Alarm set for {alarm_time}")

            if not self.is_alarm_active:
                self.is_alarm_active = True
                self.alarm_thread = threading.Thread(target=self.check_alarm)
                self.alarm_thread.start()

        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM format.")

    def check_alarm(self):
        while self.alarms:
            current_time = datetime.now().strftime("%H:%M")
            for alarm in self.alarms:
                if alarm["time"] == current_time:
                    self.play_alarm(alarm["tone"])
                    time.sleep(60)  # Prevents the alarm from triggering multiple times in the same minute
            time.sleep(1)

    def play_alarm(self, tone):
        pygame.mixer.music.load(tone)
        pygame.mixer.music.play(loops=-1)
        response = messagebox.askyesno("Alarm", "Alarm ringing! Do you want to snooze?")
        if response:
            pygame.mixer.music.stop()
            time.sleep(self.snooze_time * 60)
        else:
            pygame.mixer.music.stop()
            self.alarms.pop(0)

        if not self.alarms:
            self.is_alarm_active = False
            self.active_alarm_label.config(text="No active alarms")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
