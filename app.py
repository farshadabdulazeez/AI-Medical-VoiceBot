from dotenv import load_dotenv  # For loading environment variables from a .env file
load_dotenv()  # Load environment variables

# VoiceBot UI with Gradio
import os  # For interacting with the operating system
import gradio as gr  # For creating the user interface

# Import custom modules
from ai_medical_assistant import encode_image, analyze_image_with_query  # For image encoding and analysis
from patient_query import record_audio, transcribe_with_groq  # For audio recording and transcription
from doctor_voice_tts import text_to_speech_with_gtts, text_to_speech_with_elevenlabs  # For text-to-speech conversion


# Step 1: Define System Prompt
# This prompt guides the AI model to act like a professional doctor.
# It ensures responses are concise, human-like, and tailored for real-world interaction.
system_prompt = """You have to act as a professional doctor. Keep in mind this is for learning purposes only. 
                Do not add any numbers or special characters in your response. Your response should be in one long paragraph.
                Always answer as if you are addressing a real person. Mimic an actual doctor's tone, not an AI bot.
                If you make a differential diagnosis, suggest some remedies. Start your response immediately without preamble.
                Example: "With what I see, I think you might have... Here are some remedies..." 
                Keep your answer concise (maximum 2 sentences)."""

# Step 2: Main Function to Process Inputs
def process_inputs(audio_filepath, image_filepath):
    """
    Processes audio and image inputs, generates a doctor's response, and converts it to speech.
    
    Args:
        audio_filepath (str): Path to the recorded audio file.
        image_filepath (str): Path to the uploaded image file.
    
    Returns:
        str: Transcribed text from the audio.
        str: Doctor's response based on the analysis.
        str: Path to the generated audio file (Doctor's voice).
    """
    try:
        # Step 2a: Convert Audio to Text (Speech-to-Text)
        print("Transcribing audio...")
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),  # Retrieve API key
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        print(f"Transcription complete: {speech_to_text_output}")
    except Exception as e:
        print(f"Error during transcription: {e}")
        speech_to_text_output = "Unable to transcribe audio."

    try:
        # Step 2b: Analyze Image (if provided)
        print("Analyzing image...")
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,  # Combine system prompt with transcription
                encoded_image=encode_image(image_filepath),  # Encode the image into base64
                model="llama-3.2-11b-vision-preview"
            )
            print(f"Doctor's response: {doctor_response}")
        else:
            doctor_response = "No image provided for analysis."
            print(doctor_response)
    except Exception as e:
        print(f"Error during image analysis: {e}")
        doctor_response = "Unable to analyze the image."

    try:
        # Step 2c: Convert Doctor's Response to Speech (Text-to-Speech)
        print("Generating doctor's voice...")
        voice_of_doctor = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="final.mp3"
        )
        print("Voice generation complete.")
    except Exception as e:
        print(f"Error during voice generation: {e}")
        voice_of_doctor = None

    return speech_to_text_output, doctor_response, voice_of_doctor


# Step 3: Create Gradio Interface
# This defines the user interface for interacting with the AI doctor.
iface = gr.Interface(
    fn=process_inputs,  # Function to handle inputs
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),  # Microphone input for audio
        gr.Image(type="filepath")  # Image upload input
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),  # Display transcribed text
        gr.Textbox(label="Doctor's Response"),  # Display doctor's response
        gr.Audio(label="Doctor's Voice")  # Play the generated audio
    ],
    title="AI Doctor with Vision and Voice",  # Title of the interface
    description="Upload an image and/or record your voice to interact with the AI doctor."  # Description
)

# Step 4: Launch the Interface
if __name__ == "__main__":
    iface.launch(debug=True)  # Launch the Gradio app in debug mode