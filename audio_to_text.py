import whisper
import os

# Path to your audio file
audio_file = r"C:\Users\pawan\Downloads\Untitled notebook.wav"

# Load Whisper model
model = whisper.load_model("small")

# Transcribe audio to text
result = model.transcribe(audio_file)

# Save the transcription to a text file
output_folder = "transcriptions"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_file = os.path.join(output_folder, "transcription.txt")

with open(output_file, "w") as f:
    f.write(result["text"])

print(f"Transcription completed. The result is saved in {output_file}")
