from vosk import Model, KaldiRecognizer
import wave
import json
import os
from pydub import AudioSegment
import logging
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_to_wav(input_file, output_path="temp_audio.wav"):
    """Convert MP3/MP4 to WAV format"""
    try:
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_frame_rate(16000)  # Set sample rate to 16kHz
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        logger.error(f"Error converting file {input_file}: {str(e)}")
        raise

def transcribe_audio(audio_path, model, output_folder="transcriptions"):
    """Transcribe a single audio file to text"""
    try:
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Convert to WAV if needed
        file_ext = os.path.splitext(audio_path)[1].lower()
        temp_wav = None
        if file_ext in ['.mp3', '.mp4']:
            logger.info(f"Converting {audio_path} to WAV format...")
            temp_wav = f"temp_{int(time.time())}.wav"
            wav_path = convert_to_wav(audio_path, temp_wav)
        else:
            wav_path = audio_path

        # Process audio
        logger.info(f"Transcribing {audio_path}...")
        wf = wave.open(wav_path, "rb")
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += result['text'] + " "

        final_result = json.loads(recognizer.FinalResult())
        text += final_result['text']

        # Generate output filename based on input filename
        output_file = os.path.join(output_folder, 
                                 f"{os.path.splitext(os.path.basename(audio_path))[0]}_transcript.txt")
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(text)

        # Cleanup temporary WAV file if created
        if temp_wav and os.path.exists(temp_wav):
            os.remove(temp_wav)

        logger.info(f"Completed transcription of: {audio_path}")
        return output_file

    except Exception as e:
        logger.error(f"Error transcribing {audio_path}: {str(e)}")
        return None
    finally:
        if 'wf' in locals():
            wf.close()

def process_audio_folder(input_folder, output_folder="transcriptions"):
    """Process all audio files in a folder"""
    try:
        # Load Vosk model once for all files
        model_path = r"C:\Users\pawan\Downloads\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"  # Update this path
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model not found. Please download and update the path.")
        
        logger.info("Loading Vosk model...")
        model = Model(model_path)

        # Create output folder
        os.makedirs(output_folder, exist_ok=True)

        # Get all audio files
        audio_files = []
        for ext in ['.wav', '.mp3', '.mp4']:
            audio_files.extend(Path(input_folder).glob(f"*{ext}"))

        if not audio_files:
            logger.warning(f"No audio files found in {input_folder}")
            return

        # Process each file
        results = []
        total_files = len(audio_files)
        for idx, audio_file in enumerate(audio_files, 1):
            logger.info(f"Processing file {idx}/{total_files}: {audio_file}")
            result = transcribe_audio(str(audio_file), model, output_folder)
            results.append((str(audio_file), result))

        # Generate summary report
        summary_file = os.path.join(output_folder, "transcription_summary.txt")
        with open(summary_file, "w", encoding='utf-8') as f:
            f.write("Transcription Summary\n")
            f.write("===================\n\n")
            for audio_file, result in results:
                status = "Success" if result else "Failed"
                f.write(f"File: {audio_file}\nStatus: {status}\nOutput: {result}\n\n")

        logger.info(f"Processing completed. Summary saved to: {summary_file}")
        return summary_file

    except Exception as e:
        logger.error(f"Error processing folder: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    input_folder = r"C:\Users\pawan\Documents\Workspace\audio2text\input_folder"  # Update this path
    try:
        summary_file = process_audio_folder(input_folder)
        print(f"Processing completed. Check summary at: {summary_file}")
    except Exception as e:
        print(f"Failed to process files: {str(e)}")