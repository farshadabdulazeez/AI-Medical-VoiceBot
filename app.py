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
    # Initialize outputs
    speech_to_text_output = "No audio provided."
    doctor_response = "No analysis performed."
    temp_audio_file = None

    try:
        # Step 2a: Convert Audio to Text (Speech-to-Text)
        if audio_filepath:
            print("Transcribing audio...")
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),  # Retrieve API key
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
            print(f"Transcription complete: {speech_to_text_output}")
        else:
            speech_to_text_output = "No audio provided."
    except Exception as e:
        print(f"Error during transcription: {e}")
        speech_to_text_output = "An error occurred while transcribing the audio."

    try:
        # Step 2b: Analyze Image (if provided)
        if image_filepath:
            print("Analyzing image...")
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,  # Combine system prompt with transcription
                encoded_image=encode_image(image_filepath),  # Encode the image into base64
                model="llama-3.2-11b-vision-preview"
            )
            print(f"Doctor's response: {doctor_response}")
        else:
            doctor_response = "No image provided for analysis."
    except Exception as e:
        print(f"Error during image analysis: {e}")
        doctor_response = "An error occurred while analyzing the image."

    try:
        # Step 2c: Convert Doctor's Response to Speech (Text-to-Speech)
        print("Generating doctor's voice...")
        temp_audio_file = "temp_output.mp3"  # Temporary audio file
        text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath=temp_audio_file
        )
        print("Voice generation complete.")
    except Exception as e:
        print(f"Error during voice generation: {e}")
        temp_audio_file = None

    return speech_to_text_output, doctor_response, temp_audio_file


# Step 3: Create Gradio Interface with Enhanced UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="green", secondary_hue="gray")) as demo:
    # Heading Section
    with gr.Row():
        gr.Markdown("""
        <div id="top" style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #28a745;">🏥 AI Medical VoiceBot</h1>
            <p>Upload an image and/or record your voice to interact with the AI doctor.</p>
        </div>
        """)

    # Main Interface
    with gr.Row():
        # Fixed-size Image Upload with Scale Fit
        image_input = gr.Image(
            label="Upload an Image",
            type="filepath",
            height=300,  # Height set to 500px
            width=200,   # Width set to 200px
            scale=True   # Ensures the image fits within the container
        )
        audio_input = gr.Audio(label="Record Your Voice", sources=["microphone"], type="filepath")

    with gr.Row():
        submit_button = gr.Button("Submit", variant="primary")

    with gr.Column():
        speech_to_text_output = gr.Textbox(label="🎤 Speech to Text", lines=3)
        doctor_response_output = gr.Textbox(label="🩺 Doctor's Response", lines=5)
        doctor_voice_output = gr.Audio(label="🎧 Doctor's Voice", autoplay=False)  # Autoplay disabled initially

    def on_submit(audio_filepath, image_filepath):
        # Process inputs
        speech_to_text_output, doctor_response, temp_audio_file = process_inputs(audio_filepath, image_filepath)

        # Return outputs
        return speech_to_text_output, doctor_response, temp_audio_file

    submit_button.click(
        fn=on_submit,
        inputs=[audio_input, image_input],  # Use Gradio components here
        outputs=[speech_to_text_output, doctor_response_output, doctor_voice_output]
    )

    # Disclaimer Section at the End
    with gr.Row():
        gr.Markdown("""
        <div style="text-align: center; margin-top: 40px; background-color: #000000; padding: 15px; border-radius: 5px; border: 1px solid #c3e6cb;">
            <h2 style="color: #155724;">⚠️ Important Disclaimer</h2>
            <p>This application is for educational and demonstration purposes only. It is not intended to provide medical advice or replace professional healthcare services. The responses generated by this app are not a substitute for consulting a licensed healthcare provider. Always seek professional medical advice for any health concerns.</p>
            <p><a href="#top" style="color: #28a745; text-decoration: none;">Back to Top</a></p>
        </div>
        """)

# Step 4: Launch the Interface
if __name__ == "__main__":
    demo.launch(debug=True, share=True)