import whisper
import pyaudio
import wave
import os

# Load Whisper model (using "tiny" for faster results)
model = whisper.load_model("tiny")

# Audio settings for live recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # Duration of each audio chunk

# Folder to save transcriptions
output_folder = "transcriptions"
os.makedirs(output_folder, exist_ok=True)

def transcribe_recorded(audio_file_path):
    """Transcribes a pre-recorded audio file"""
    print("Transcribing recorded audio...")
    result = model.transcribe(audio_file_path)
    
    # Save the transcription to a file
    output_file = os.path.join(output_folder, "recorded_transcription.txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
    
    print(f"Recorded transcription completed. Saved to {output_file}")

def transcribe_live():
    """Captures live audio and transcribes it in real-time"""
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening... You can speak now. Press Ctrl+C to stop.")

    try:
        while True:
            # Capture audio in chunks
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            # Save the audio chunk as a temporary .wav file
            temp_audio_file = "temp_audio.wav"
            wf = wave.open(temp_audio_file, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Transcribe the audio chunk
            result = model.transcribe(temp_audio_file)

            # Print and save the transcription
            transcription = result["text"]
            print(f"Live Transcription: {transcription}")

            # Save transcription to a file
            output_file = os.path.join(output_folder, "live_transcription.txt")
            with open(output_file, "a") as f:
                f.write(transcription + "\n")

            # Delete the temporary audio file
            os.remove(temp_audio_file)

    except KeyboardInterrupt:
        print("\nStopped listening.")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    # Choose between recorded and live transcription
    choice = input("Choose mode - (R)ecorded or (L)ive transcription: ").strip().lower()

    if choice == 'r':
        audio_file_path = input('Enter the path to your audio file (e.g., C:\\Users\\pawan\\Downloads\\Untitled notebook.wav): ').strip()
        transcribe_recorded(audio_file_path)
    elif choice == 'l':
        transcribe_live()
    else:
        print("Invalid choice. Please enter 'R' for recorded or 'L' for live transcription.")
