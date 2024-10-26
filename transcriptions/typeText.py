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

# Function to type the content with pause and resume functionality
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

# Event handler to pause typing
def pause_typing():
    global is_typing_paused
    is_typing_paused = True
    print("Typing paused. Press 's' to resume.")

# Event handler to resume typing
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

# Main typing function that waits for Spacebar before starting
def start_typing():
    global is_script_running
    content = read_file_content(file_path)
    if content:
        print("Move your cursor to the desired editor window and position it in the typing area.")
        print("Press Spacebar to start typing once your cursor is positioned correctly.")
        print("Hotkeys: 'a' to pause, 's' to resume, 'd' to terminate.")

        # Wait for Spacebar press to confirm cursor position
        keyboard.wait('space')
        print("Starting typing...")

        # Start typing content
        type_text_with_pause(content, typing_speed)

# Run the typing function in a separate thread to allow hotkeys to work simultaneously
typing_thread = threading.Thread(target=start_typing)
typing_thread.start()
