import tkinter as tk
from tkinter import ttk, messagebox
import time

# Sample texts for different levels
text_samples = {
    "Low": "The quick brown fox jumps over the lazy dog.",
    "Medium": "Typing fast can improve your productivity and save time for many tasks.",
    "High": "The complexities of the typing test challenge will push your speed and accuracy to new levels."
}

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFFFFF")  # White background
        self.root.resizable(False, False)

        # Initialize variables
        self.selected_stage = tk.StringVar(value="Low")
        self.test_text = ""
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.timer_id = None
        self.timer_started = False  # To ensure timer starts on first keypress

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme for better styling

        # Configure styles
        self.configure_styles()

        # Create the main UI
        self.create_ui()

    def configure_styles(self):
        # Title Style
        self.style.configure("Title.TLabel",
                             foreground="#000000",
                             background="#FFFFFF",
                             font=("Helvetica", 28, "bold"))

        # Label Style
        self.style.configure("TLabel",
                             foreground="#000000",
                             background="#FFFFFF",
                             font=("Helvetica", 14))

        # Combobox Style
        self.style.configure("TCombobox",
                             foreground="#000000",
                             font=("Helvetica", 12),
                             fieldbackground="#FFFFFF",
                             background="#FFFFFF")
        self.style.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')])

        # Button Style
        self.style.configure("TButton",
                             foreground="#000000",
                             background="#F0F0F0",
                             font=("Helvetica", 12, "bold"),
                             padding=6)
        self.style.map('TButton',
                       background=[('active', '#E0E0E0')],
                       foreground=[('active', '#000000')])

        # Entry Style
        self.style.configure("TEntry",
                             foreground="#000000",
                             font=("Helvetica", 14),
                             fieldbackground="#FFFFFF")

        # Hover Style for Buttons
        self.style.configure("Hover.TButton",
                             foreground="#000000",
                             background="#E0E0E0",
                             font=("Helvetica", 12, "bold"),
                             padding=6)

    def create_ui(self):
        # Title Label
        title_label = ttk.Label(self.root, text="Typing Speed Test", style="Title.TLabel")
        title_label.pack(pady=20)

        # Timer Label
        self.timer_label = ttk.Label(self.root, text="Time: 0s", style="TLabel")
        self.timer_label.pack()

        # Frame for stage selection
        stage_frame = ttk.Frame(self.root, padding=10)
        stage_frame.pack(pady=10)

        stage_label = ttk.Label(stage_frame, text="Choose Stage:", style="TLabel")
        stage_label.pack(side=tk.LEFT, padx=(0, 10))

        stage_dropdown = ttk.Combobox(stage_frame,
                                      textvariable=self.selected_stage,
                                      values=list(text_samples.keys()),
                                      state="readonly",
                                      width=15)
        stage_dropdown.pack(side=tk.LEFT)
        stage_dropdown.current(0)  # Set default selection to "Low"

        # Text display area with a frame
        text_frame = ttk.Frame(self.root, padding=10)
        text_frame.pack(pady=20)

        text_label = ttk.Label(text_frame, text="Type the following text:", style="TLabel")
        text_label.pack(anchor='w')

        # Using Label instead of Text for better visibility
        self.text_display = ttk.Label(text_frame,
                                      text="",  # Initially empty
                                      wraplength=700,
                                      justify="center",
                                      font=("Helvetica", 14),
                                      background="#FFFFFF",
                                      foreground="#000000")
        self.text_display.pack(pady=10)

        # Entry for typing test
        entry_frame = ttk.Frame(self.root, padding=10)
        entry_frame.pack(pady=10)

        typing_label = ttk.Label(entry_frame, text="Your Input:", style="TLabel")
        typing_label.pack(anchor='w')

        self.typing_entry = ttk.Entry(entry_frame,
                                      width=70,
                                      font=("Helvetica", 14),
                                      style="TEntry")
        self.typing_entry.pack(pady=5)
        self.typing_entry.bind("<Return>", self.stop_test)
        self.typing_entry.bind("<Key>", self.start_timer_on_keypress)

        # Frame for buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(pady=20)

        start_button = ttk.Button(button_frame, text="Start Test", command=self.start_test)
        start_button.pack(side=tk.LEFT, padx=20)

        stop_button = ttk.Button(button_frame, text="Stop Test", command=self.stop_test)
        stop_button.pack(side=tk.LEFT, padx=20)

        quit_button = ttk.Button(button_frame, text="Quit", command=self.root.quit)
        quit_button.pack(side=tk.LEFT, padx=20)

        # Footer Label
        footer_label = ttk.Label(self.root, text="Developed with Tkinter", style="TLabel")
        footer_label.pack(side=tk.BOTTOM, pady=10)

        # Adding simple animations: Hover effects for buttons
        for widget in button_frame.winfo_children():
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget['style'] = 'Hover.TButton'

    def on_leave(self, event):
        event.widget['style'] = 'TButton'

    def start_test(self):
        # If a test is already running, do not start another
        if self.timer_running:
            messagebox.showinfo("Info", "Test is already running.", parent=self.root)
            return

        # Retrieve the text for the selected stage
        stage = self.selected_stage.get()
        self.test_text = text_samples.get(stage, "")

        if not self.test_text:
            messagebox.showerror("Error", "Selected stage has no text.")
            return

        # Clear previous typing entry and display the new text
        self.typing_entry.delete(0, tk.END)
        self.typing_entry.focus_set()
        self.text_display.config(text=self.test_text)

        # Reset and start the timer
        self.elapsed_time = 0
        self.timer_label.config(text=f"Time: {self.elapsed_time}s")
        self.timer_running = True
        self.timer_started = False  # Reset to start timer on first keypress

        # Record the start time as None until typing starts
        self.start_time = None

    def start_timer_on_keypress(self, event):
        if not self.timer_running:
            return
        if not self.timer_started:
            self.start_time = time.time()
            self.timer_started = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running and self.timer_started:
            current_time = time.time()
            self.elapsed_time = int(current_time - self.start_time)
            self.timer_label.config(text=f"Time: {self.elapsed_time}s")
            # Schedule the timer to update every second
            self.timer_id = self.root.after(1000, self.update_timer)

    def stop_test(self, event=None):
        if not self.timer_running:
            messagebox.showerror("Error", "Please start the test first!", parent=self.root)
            return

        # Stop the timer
        self.timer_running = False
        self.timer_started = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Calculate the elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = self.elapsed_time  # In case timer was not started

        typed_text = self.typing_entry.get()

        # Check typing accuracy
        accuracy = self.calculate_accuracy(typed_text, self.test_text)

        # Display results
        self.show_results(elapsed_time, accuracy)

        # Reset start time
        self.start_time = None

    def calculate_accuracy(self, typed_text, original_text):
        correct_chars = sum(1 for a, b in zip(typed_text, original_text) if a == b)
        total_chars = len(original_text)
        return (correct_chars / total_chars) * 100 if total_chars > 0 else 0

    def show_results(self, time_taken, accuracy):
        # Calculate words per minute (WPM)
        words = len(self.test_text.split())
        wpm = (words / time_taken) * 60 if time_taken > 0 else 0

        # Show results in a pop-up window
        result_window = tk.Toplevel(self.root)
        result_window.title("Test Results")
        result_window.geometry("400x300")
        result_window.configure(bg="#FFFFFF")  # White background
        result_window.resizable(False, False)

        # Configure styles for result window
        result_style = ttk.Style()
        result_style.theme_use('clam')
        result_style.configure("Result.TLabel",
                               foreground="#000000",
                               background="#FFFFFF",
                               font=("Helvetica", 14))
        result_style.configure("ResultTitle.TLabel",
                               foreground="#000000",
                               background="#FFFFFF",
                               font=("Helvetica", 18, "bold"))

        # Title
        result_title = ttk.Label(result_window, text="Your Results", style="ResultTitle.TLabel")
        result_title.pack(pady=20)

        # Time Taken
        time_label = ttk.Label(result_window, text=f"Time Taken: {time_taken:.2f} seconds", style="Result.TLabel")
        time_label.pack(pady=10)

        # Accuracy
        accuracy_label = ttk.Label(result_window, text=f"Accuracy: {accuracy:.2f}%", style="Result.TLabel")
        accuracy_label.pack(pady=10)

        # WPM
        wpm_label = ttk.Label(result_window, text=f"Speed: {wpm:.2f} WPM", style="Result.TLabel")
        wpm_label.pack(pady=10)

        # Close Button
        close_button = ttk.Button(result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=20)
        close_button.bind("<Enter>", self.on_enter)
        close_button.bind("<Leave>", self.on_leave)

    # Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
