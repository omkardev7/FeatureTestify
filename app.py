import streamlit as st
from dotenv import load_dotenv
import warnings
import os

groq_api_key = os.getenv("GROQ_API_KEY")
warnings.filterwarnings("ignore")

from groq import Groq
import base64

# Initialize the Groq client with your API key
client = Groq(api_key='YOUR_GROQ_API_KEY')

llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

# Set up the page layout
st.title("Testing Instruction Generator")
st.write("Upload screenshots and provide optional context to generate testing instructions.")

# User input for context and screenshots
context = st.text_input("Enter optional context for testing:")
uploaded_files = st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Button to trigger testing instruction generation
if st.button("Describe Testing Instructions") and uploaded_files:
    # Process the images and generate instructions
    st.write("Processing...")

    # Call the functions to handle images and generate instructions here...
else:
    st.warning("Please upload at least one screenshot to proceed.")
    
# Function to encode images to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_text(client, model, base64_image, prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model=model
    )

    return chat_completion.choices[0].message.content

def generate_testing_instructions(client, image_description):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a QA expert. Create a detailed test plan based on the description provided.",
            },
            {
                "role": "user",
                "content": image_description,
            }
        ],
        model=llama31_model
    )
    
    return chat_completion.choices[0].message.content

if st.button("Describe Testing Instructions") and uploaded_files:
    st.write("Processing...")

    # Loop through each uploaded file and process
    descriptions = []
    for uploaded_file in uploaded_files:
        base64_image = encode_image(uploaded_file)
        description = image_to_text(client, llava_model, base64_image, "Describe the functionality in this screenshot.")
        descriptions.append(description)

    # Concatenate all descriptions into a single input
    combined_description = " ".join(descriptions)
    
    # Generate testing instructions
    testing_instructions = generate_testing_instructions(client, combined_description)
    
    # Display the generated instructions
    st.write(testing_instructions)
