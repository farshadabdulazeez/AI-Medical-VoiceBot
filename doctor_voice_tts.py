# Import necessary libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
load_dotenv()  # Load environment variables

import os  # For interacting with the operating system
from gtts import gTTS  # Google Text-to-Speech library
from elevenlabs.client import ElevenLabs  # ElevenLabs TTS generation
import subprocess  # For playing audio files
import platform  # For detecting the operating system

# Step 1a: Setup Text-to-Speech (TTS) model with gTTS
def text_to_speech_with_gtts_old(input_text, output_filepath):
    """
    Converts text to speech using gTTS and saves the audio file.
    Args:
        input_text (str): The text to convert to speech.
        output_filepath (str): The path to save the generated audio file.
    """
    if not input_text or not isinstance(input_text, str):
        print("Error: Invalid input text.")
        return

    print("Starting gTTS conversion...")
    language = "en"  # Language for TTS
    try:
        print(f"Creating gTTS object with text: {input_text}")
        audioobj = gTTS(
            text=input_text,
            lang=language,
            slow=False  # Normal speed
        )
        print(f"Saving audio file to {output_filepath}...")
        audioobj.save(output_filepath)  # Save the audio file
        print("Audio file saved successfully.")
    except Exception as e:
        print(f"An error occurred during gTTS conversion: {e}")


# Step 1b: Setup Text-to-Speech (TTS) model with ElevenLabs
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    """
    Converts text to speech using ElevenLabs and saves the audio file.
    Args:
        input_text (str): The text to convert to speech.
        output_filepath (str): The path to save the generated audio file.
    """
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")  # Retrieve API key
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is missing. Please check your .env file.")
    
    from elevenlabs.client import ElevenLabs  # Import the ElevenLabs client

    print("Starting ElevenLabs TTS conversion...")
    try:
        # Initialize the ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio = client.generate(
            text=input_text,
            voice="Aria",  # Voice model
            model="eleven_turbo_v2"  # Model version
        )
        print(f"Saving audio file to {output_filepath}...")
        
        # Save the audio file
        with open(output_filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)  # Write audio chunks to the file
        print("Audio file saved successfully.")
    except Exception as e:
        print(f"An error occurred during ElevenLabs TTS conversion: {e}")


# Example usage for gTTS (uncomment to test)
# input_text = "Hi, How have you been, autoplay testing!"
# output_filepath = "gtts_testing.mp3"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath=output_filepath)

# Example usage for ElevenLabs (uncomment to test)
# input_text = "Hi, How have you been, autoplay testing!"
# output_filepath = "elevenlabs_testing.mp3"
# text_to_speech_with_elevenlabs_old(input_text, output_filepath=output_filepath)

# Step 2: Use Model for Text Output to Voice with Autoplay
def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Converts text to speech using gTTS, saves the audio file, and plays it automatically.
    Args:
        input_text (str): The text to convert to speech.
        output_filepath (str): The path to save the generated audio file.
    """
    language = "en"  # Language for TTS
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False  # Normal speed
    )
    audioobj.save(output_filepath)  # Save the audio file
    
    # Play the audio file based on the operating system
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Example usage for gTTS with autoplay (uncomment to test)
# input_text = "Hi, How have you been, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Converts text to speech using ElevenLabs, saves the audio file, and plays it automatically.
    Args:
        input_text (str): The text to convert to speech.
        output_filepath (str): The path to save the generated audio file.
    """
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")  # Retrieve API key
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is missing. Please check your .env file.")
    
    print("Starting ElevenLabs TTS conversion...")
    try:
        # Initialize the ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio = client.generate(
            text=input_text,
            voice="Aria",  # Voice model
            model="eleven_turbo_v2"  # Model version
        )
        print(f"Saving audio file to {output_filepath}...")
        
        # Save the audio file
        with open(output_filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)  # Write audio chunks to the file
        print("Audio file saved successfully.")
    except Exception as e:
        print(f"An error occurred during ElevenLabs TTS conversion: {e}")
        return

    # Play the audio file based on the operating system
    os_name = platform.system()
    try:
        print("Playing audio file...")
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
        print("Audio playback complete.")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Example usage for ElevenLabs with autoplay (uncomment to test)
# input_text = "Hi, How have you been, autoplay testing!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")