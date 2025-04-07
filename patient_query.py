from dotenv import load_dotenv  # For loading environment variables from a .env file
load_dotenv()

# Step 1: Setup Audio Recorder (ffmpeg & portaudio)
# Dependencies: ffmpeg, portaudio, pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.
    Requires `speech_recognition`, `pydub`, and `ffmpeg`.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts for background noise
            logging.info("Start speaking now...")
            
            # Record the audio using the microphone
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to WAV format and then export as MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))  # Convert to AudioSegment
            audio_segment.export(file_path, format="mp3", bitrate="128k")  # Export as MP3
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Path to save the recorded audio file
audio_filepath = "patient_voice_test_for_patient.mp3"

# Uncomment the line below to test audio recording
# record_audio(file_path=audio_filepath)

# Step 2: Setup Speech-to-Text (STT) Model for Transcription
import os
from groq import Groq

# Retrieve GROQ_API_KEY from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    logging.error("ERROR: GROQ_API_KEY is missing. Please check your .env file.")
    exit(1)

stt_model = "whisper-large-v3"  # Specify the STT model to use

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Function to transcribe audio using Groq's Whisper model.
    Requires an API key and the path to the audio file.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)  # Initialize Groq client with API key
        
        # Open the audio file and send it to Groq for transcription
        with open(audio_filepath, "rb") as audio_file:
            logging.info("Transcribing audio...")
            transcription = client.audio.transcriptions.create(
                model=stt_model,  # Specify the model (e.g., whisper-large-v3)
                file=audio_file,  # Pass the audio file
                language="en"  # Specify the language (English in this case)
            )
        
        logging.info("Transcription complete.")
        return transcription.text  # Return the transcribed text

    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return None

# Example usage of the transcription function
# Uncomment the lines below to test transcription
transcript = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
print(f"Transcription: {transcript}")

# Combined Test: Record audio and transcribe it
# if __name__ == "__main__":
#     # Step 1: Record audio
#     logging.info("Starting audio recording...")
#     record_audio(file_path=audio_filepath)
    
#     # Step 2: Transcribe the recorded audio
#     logging.info("Starting transcription...")
#     transcript = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
#     if transcript:
#         logging.info(f"Transcription: {transcript}")
#     else:
#         logging.error("Transcription failed.")