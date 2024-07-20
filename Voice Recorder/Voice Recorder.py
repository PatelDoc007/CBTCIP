import tkinter as tk
import sounddevice as sd
import wavio
import time


class VoiceRecorder:
    def __init__(self, master):
        self.master = master
        master.title("Voice Recorder")

        # Custom colors
        self.background_color = "#A9A9A9"  # Grey background
        self.button_color = "#4CAF50"  # Green
        self.pause_color = "#FFC107"  # Orange
        self.resume_color = "#2196F3"  # Blue
        self.stop_color = "#f44336"  # Red
        self.button_text_color = "black"  # Button text color
        self.clicked_button_color = "white"  # Color when button is clicked

        # Configure window background color
        master.configure(bg=self.background_color)

        # Create a frame for better layout control
        self.frame = tk.Frame(master, bg=self.background_color)
        self.frame.pack()

        # Buttons with custom styling
        self.button_width = 15
        self.button_height = 2
        self.button_font = ("Helvetica", 12, "bold")

        self.start_button = tk.Button(self.frame, text="Start Recording", command=self.start_recording,
                                      bg=self.button_color, fg=self.button_text_color,
                                      font=self.button_font, width=self.button_width, height=self.button_height)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        self.start_button.bind("<Button-1>", lambda event, btn=self.start_button: self.change_button_color(btn))

        self.stop_button = tk.Button(self.frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED,
                                     bg=self.stop_color, fg=self.button_text_color,
                                     font=self.button_font, width=self.button_width, height=self.button_height)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        self.stop_button.bind("<Button-1>", lambda event, btn=self.stop_button: self.change_button_color(btn))

        self.pause_button = tk.Button(self.frame, text="Pause Recording", command=self.pause_recording, state=tk.DISABLED,
                                      bg=self.pause_color, fg=self.button_text_color,
                                      font=self.button_font, width=self.button_width, height=self.button_height)
        self.pause_button.grid(row=1, column=0, padx=10, pady=10)
        self.pause_button.bind("<Button-1>", lambda event, btn=self.pause_button: self.change_button_color(btn))

        self.resume_button = tk.Button(self.frame, text="Resume Recording", command=self.resume_recording, state=tk.DISABLED,
                                       bg=self.resume_color, fg=self.button_text_color,
                                       font=self.button_font, width=self.button_width, height=self.button_height)
        self.resume_button.grid(row=1, column=1, padx=10, pady=10)
        self.resume_button.bind("<Button-1>", lambda event, btn=self.resume_button: self.change_button_color(btn))

        # Timer label
        self.timer_label = tk.Label(self.frame, text="00:00:00", font=("Helvetica", 14))
        self.timer_label.grid(row=2, columnspan=2, padx=10, pady=10)

        # Recorder parameters
        self.filename = 'recorded.wav'
        self.sample_rate = 44100
        self.audio_data = []
        self.stream = None
        self.is_recording = False
        self.is_paused = False
        self.paused_frames = []
        self.start_time = None
        self.total_elapsed_time = 0
        self.pause_start_time = None
        self.total_pause_duration = 0

    def change_button_color(self, button):
        # Change background color of the clicked button and reset others to default
        self.start_button.config(bg=self.button_color)
        self.stop_button.config(bg=self.stop_color)
        self.pause_button.config(bg=self.pause_color)
        self.resume_button.config(bg=self.resume_color)

        # Change background color of clicked button to white
        button.config(bg=self.clicked_button_color)

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)

        print("Recording...")
        self.start_time = time.time()
        self.update_timer()
        self.stream = sd.InputStream(callback=self.callback)
        self.stream.start()
        self.is_recording = True

    def pause_recording(self):
        if self.is_recording and not self.is_paused:
            self.is_paused = True
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            self.pause_start_time = time.time()  # Start pause timer

    def resume_recording(self):
        if self.is_recording and self.is_paused:
            self.is_paused = False
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.total_pause_duration += time.time() - self.pause_start_time  # Accumulate pause duration
            self.update_timer()

    def stop_recording(self):
        if self.stream:
            self.stream.stop()
            self.stream = None
            self.is_recording = False
            self.total_elapsed_time = 0
            self.total_pause_duration = 0
            self.timer_label.config(text="00:00:00")  # Reset timer label

        print("Recording stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

        # Save audio
        if self.audio_data:
            print("Saving recording to", self.filename)
            wavio.write(self.filename, self.audio_data, self.sample_rate, sampwidth=2)
            print("Recording saved as", self.filename)
            self.audio_data = []  # Clear audio data after saving

    def callback(self, indata, frames, time, status):
        if self.is_recording and not self.is_paused:
            self.audio_data.append(indata.copy())
            self.update_timer()

    def update_timer(self):
        if self.is_recording and not self.is_paused:
            current_time = time.time()
            elapsed_time = current_time - self.start_time - self.total_pause_duration
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            self.timer_label.config(text="{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
            self.timer_label.after(100, self.update_timer)  # Update every 100ms while recording

    def cleanup(self):
        if self.stream:
            self.stream.stop()
            self.stream = None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x220")  # Set initial size of the window
    recorder = VoiceRecorder(root)
    root.protocol("WM_DELETE_WINDOW", recorder.cleanup)  # Handle closing of the window
    root.mainloop()
