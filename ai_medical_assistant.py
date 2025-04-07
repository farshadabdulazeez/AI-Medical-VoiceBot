# Import necessary libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For interacting with the operating system (e.g., accessing environment variables)
import base64  # For encoding images into base64 format

# Load environment variables from a .env file (if present)
load_dotenv()

# Step 1: Setup GROQ API key
# Retrieve the GROQ_API_KEY from the environment variables.
# This key is required to authenticate requests to the Groq API.
# Retrieve API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing. Please check your .env file.")
    exit(1)
else:
    print("GROQ API Key successfully loaded.")

# Step 2: Convert image to required format
# Function to encode an image file into base64 format.
# This is necessary because the Groq API expects images in base64-encoded format.
def encode_image(image_path):
    # Open the image file in binary mode ("rb").
    with open(image_path, "rb") as image_file:
        # Read the file content, encode it in base64, and decode it to a UTF-8 string.
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup Multimodal LLM
# Import the Groq client library to interact with the Groq API.
from groq import Groq

# Define a query for the AI model to analyze the image.
# This query will guide the model on what to look for in the image.
query = "Is there something wrong with my face?"

# Specify the model to use for the analysis.
# In this case, we are using the "llama-3.2-90b-vision-preview" multimodal model.
model = "llama-3.2-90b-vision-preview"

# Function to analyze an image with a given query.
# This function sends a request to the Groq API with the query and the encoded image.
def analyze_image_with_query(query, model, encoded_image):
    # Initialize the Groq client with the API key.
    client = Groq(api_key=GROQ_API_KEY)  # Pass the API key here
    
    # Prepare the messages payload for the API request.
    # The payload includes both text (query) and image data (base64-encoded image).
    messages = [
        {
            "role": "user",  # Indicates that this message is from the user.
            "content": [
                {
                    "type": "text",  # The first part of the message is the query text.
                    "text": query
                },
                {
                    "type": "image_url",  # The second part of the message is the image data.
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",  # Base64-encoded image URL.
                    },
                },
            ],
        }
    ]
    
    # Send the chat completion request to the Groq API.
    chat_completion = client.chat.completions.create(
        messages=messages,  # Pass the prepared messages payload.
        model=model  # Specify the model to use for processing.
    )
    
    # Extract and return the model's response.
    return chat_completion.choices[0].message.content

# Main Execution Block
if __name__ == "__main__":
    # Path to the input image (relative path within the project directory)
    image_path = "acne.webp"  # Replace with your image file name
    
    # Encode the image into base64 format
    try:
        encoded_image = encode_image(image_path)
        print("Image successfully encoded.")
    except FileNotFoundError:
        print(f"Error: The image file '{image_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"Error encoding image: {e}")
        exit(1)
    
    # Analyze the image with the query
    try:
        response = analyze_image_with_query(query, model, encoded_image)
        print("Response from the model:")
        print(response)
    except Exception as e:
        print(f"Error analyzing image: {e}")