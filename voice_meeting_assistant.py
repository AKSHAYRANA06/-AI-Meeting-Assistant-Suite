import tkinter as tk
from tkinter import scrolledtext, messagebox, Frame, Label, Button
import speech_recognition as sr
import threading
import datetime


def summarize_text(text, max_sentences=3):
    """
    A very simple text summarizer.
    Picks the first, middle, and last sentences.
    """
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= max_sentences:
        return text

    summary = []
    summary.append(sentences[0])  # First sentence
    if len(sentences) > 2:
        summary.append(sentences[len(sentences)//2])  # Middle
    summary.append(sentences[-1])  # Last sentence

    return ". ".join(summary) + "."


recording = False
rec_text = ""

def start_recording(status_label):
    """
    Starts the voice recording thread.
    Updates the status label.
    """
    global recording, rec_text
    if recording:
        messagebox.showwarning("Recording", "Recording is already in progress!")
        return
        
    recording = True
    rec_text = ""
    status_label.config(text="Status: Recording...", fg="#f44336")
    threading.Thread(target=record_voice_thread, args=(status_label,), daemon=True).start()

def stop_recording(status_label):
    """
    Stops the voice recording thread.
    Updates the status label.
    """
    global recording
    if not recording:
        messagebox.showinfo("Stopped", "Recording is not in progress.")
        return

    recording = False
    status_label.config(text="Status: Idle", fg="#6c757d")
    messagebox.showinfo("Stopped", "Voice recording stopped!")

def record_voice_thread(status_label):
    """
    The background thread that listens for voice.
    """
    global recording, rec_text, text_box

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

            while recording:
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio)
                    rec_text += " " + text

                    # Update GUI from the thread safely
                    text_box.insert(tk.END, text + " ")
                    text_box.see(tk.END)

                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.WaitTimeoutError:
                    # No speech detected in the timeout period
                    pass
                except Exception as e:
                    print(f"Error in recording loop: {e}")

    except Exception as e:
        print(f"Microphone error: {e}")
        messagebox.showerror("Error", "Could not find a microphone. Please check your device.")
        status_label.config(text="Status: Error", fg="#dc3545")
        
    # When loop finishes (recording set to False)
    status_label.config(text="Status: Idle", fg="#6c757d")


def save_file():
    """
    Saves the full text and summary to a new text file.
    """
    full_text = text_box.get("1.0", tk.END).strip()
    summary = summary_box.get("1.0", tk.END).strip()

    if not full_text and not summary:
        messagebox.showwarning("Empty", "There is nothing to save!")
        return

    fname = "meeting_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    try:
        with open(fname, "w", encoding="utf-8") as f:
            f.write("--- FULL TEXT ---\n")
            f.write(full_text + "\n\n")
            f.write("--- SUMMARY ---\n")
            f.write(summary)

        messagebox.showinfo("Saved", f"Meeting notes saved as {fname}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")


def generate_summary():
    """
    Gets text from the input box and puts a summary in the output box.
    """
    full_text = text_box.get("1.0", tk.END).strip()

    if not full_text:
        messagebox.showerror("Error", "No text to summarize!")
        return

    summary = summarize_text(full_text)
    summary_box.delete("1.0", tk.END)
    summary_box.insert(tk.END, summary)

# ----------------- GUI STYLING UTILITIES -----------------

def on_enter(e):
    """Changes button color on hover"""
    e.widget.config(bg=e.widget.hover_color)

def on_leave(e):
    """Changes button color back on leave"""
    e.widget.config(bg=e.widget.original_color)

def create_styled_button(parent, text, command, bg_color, hover_color):
    """Helper function to create a styled button with hover effects"""
    btn = tk.Button(parent,
                    text=text,
                    command=command,
                    font=("Segoe UI", 12, "bold"),
                    bg=bg_color,
                    fg="#ffffff",
                    activebackground=hover_color,
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    pady=8,
                    padx=12)
    
    # Store colors for hover events
    btn.original_color = bg_color
    btn.hover_color = hover_color
    
    # Bind hover events
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

# ---------------- GUI ----------------
# (This part has been completely rebuilt for a better UI)
BG_COLOR = "#212529"      # Dark background
TEXT_BG = "#343a40"      # Lighter dark for text boxes
FG_COLOR = "#e9ecef"      # Light grey text
BORDER_COLOR = "#495057"  # Subtle border color
ACCENT_BLUE = "#0d6efd"   # Summarize button
BLUE_HOVER = "#0b5ed7"
ACCENT_GREEN = "#198754"  # Start button
GREEN_HOVER = "#157347"
ACCENT_RED = "#dc3545"    # Stop button
RED_HOVER = "#bb2d3b"
ACCENT_PURPLE = "#6f42c1" # Save button
PURPLE_HOVER = "#59369a"

# --- Window Setup ---
window = tk.Tk()
window.title("AI Meeting Assistant - Modern UI")
window.geometry("900x700")
window.configure(bg=BG_COLOR)
window.minsize(600, 500)

# --- Main Frame ---
main_frame = Frame(window, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# --- Title ---
title = Label(main_frame,
              text="AI Meeting Assistant",
              font=("Segoe UI", 24, "bold"),
              bg=BG_COLOR,
              fg=FG_COLOR)
title.pack(pady=(0, 20))

# --- Status Label ---
status_label = Label(main_frame,
                     text="Status: Idle",
                     font=("Segoe UI", 11, "italic"),
                     bg=BG_COLOR,
                     fg="#6c757d") # Muted text color
status_label.pack(anchor="w", pady=(0, 5))

# --- Text Input Area ---
label1 = Label(main_frame,
               text="Meeting Text / Voice Notes:",
               font=("Segoe UI", 12),
               bg=BG_COLOR,
               fg=FG_COLOR)
label1.pack(anchor="w")

text_box = scrolledtext.ScrolledText(main_frame,
                                     width=95,
                                     height=15,
                                     font=("Segoe UI", 11),
                                     bg=TEXT_BG,
                                     fg=FG_COLOR,
                                     relief="flat",
                                     bd=0,
                                     highlightthickness=1,
                                     highlightbackground=BORDER_COLOR,
                                     insertbackground=FG_COLOR, # Text cursor color
                                     padx=10,
                                     pady=10)
text_box.pack(pady=5, expand=True, fill="both")

# --- Button Frame ---
button_frame = Frame(main_frame, bg=BG_COLOR)
button_frame.pack(pady=15, fill="x", anchor="center")
button_frame.columnconfigure((0, 1, 2, 3), weight=1) # Make buttons expand

# --- Styled Buttons ---
b1 = create_styled_button(button_frame, "Start Recording", 
                          lambda: start_recording(status_label), 
                          ACCENT_GREEN, GREEN_HOVER)
b1.grid(row=0, column=0, padx=5, sticky="ew")

b2 = create_styled_button(button_frame, "Stop Recording", 
                          lambda: stop_recording(status_label), 
                          ACCENT_RED, RED_HOVER)
b2.grid(row=0, column=1, padx=5, sticky="ew")

b3 = create_styled_button(button_frame, "Summarize Text", 
                          generate_summary, 
                          ACCENT_BLUE, BLUE_HOVER)
b3.grid(row=0, column=2, padx=5, sticky="ew")

b4 = create_styled_button(button_frame, "Save Notes", 
                          save_file, 
                          ACCENT_PURPLE, PURPLE_HOVER)
b4.grid(row=0, column=3, padx=5, sticky="ew")

# --- Summary Box ---
label2 = Label(main_frame,
               text="Summary:",
               font=("Segoe UI", 12),
               bg=BG_COLOR,
               fg=FG_COLOR)
label2.pack(anchor="w", pady=(10, 0))

summary_box = scrolledtext.ScrolledText(main_frame,
                                        width=95,
                                        height=10,
                                        font=("Segoe UI", 11),
                                        bg=TEXT_BG,
                                        fg=FG_COLOR,
                                        relief="flat",
                                        bd=0,
                                        highlightthickness=1,
                                        highlightbackground=BORDER_COLOR,
                                        insertbackground=FG_COLOR,
                                        padx=10,
                                        pady=10)
summary_box.pack(pady=5, expand=True, fill="both")

# --- Run GUI ---
window.mainloop()