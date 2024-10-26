import pyautogui
import time
import keyboard  # For detecting key presses
import threading

# File path (as specified)
file_path = r'C:\Users\pawan\Documents\Workspace\audio2text\type.txt'

# Delay between each character (in seconds)
typing_speed = 0.1  # Adjust this for faster or slower typing

# Global variables
is_typing_paused = False
is_script_running = True

# Function to read content from the file
def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None

# Function to handle typing with pause/resume
def type_text_with_pause(content, typing_speed):
    global is_typing_paused, is_script_running
    for char in content:
        if not is_script_running:  # Stop if the script is killed
            print("Script execution stopped.")
            return

        # Wait if typing is paused
        while is_typing_paused:
            time.sleep(0.1)  # Small delay to check again

        # Type the character at the current cursor position
        pyautogui.typewrite(char)
        time.sleep(typing_speed)

# Event handler to pause typing and allow manual typing
def pause_typing():
    global is_typing_paused
    is_typing_paused = True
    print("Typing paused. You can now type manually. Press 's' to resume.")

# Event handler to resume typing and block manual typing
def resume_typing():
    global is_typing_paused
    is_typing_paused = False
    print("Typing resumed.")

# Event handler to stop the script
def stop_script():
    global is_script_running
    is_script_running = False
    print("Script execution stopped.")

# Set up hotkeys with suppression
keyboard.add_hotkey('a', pause_typing, suppress=True)    # 'a' to pause
keyboard.add_hotkey('s', resume_typing, suppress=True)   # 's' to resume
keyboard.add_hotkey('d', stop_script, suppress=True)     # 'd' to stop the script

# Function to start typing in a separate thread
def start_typing():
    global is_script_running
    is_script_running = True
    content = read_file_content(file_path)
    if content:
        type_text_with_pause(content, typing_speed)

# Start typing in a separate thread to allow hotkeys to work simultaneously
typing_thread = threading.Thread(target=start_typing)
typing_thread.start()
