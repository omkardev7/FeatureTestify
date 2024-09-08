import streamlit as st
from dotenv import load_dotenv
import warnings
import os
from groq import Groq
import base64

# Load environment variables
load_dotenv()

# Retrieve the API key from the environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY is not set. Please set the API key in your environment variables.")
else:
    # Initialize Groq API client with the API key
    client = Groq(api_key=groq_api_key)
    llava_model = 'llava-v1.5-7b-4096-preview'
    llama31_model = 'llama-3.1-70b-versatile'

    # Function to encode image to base64
    def encode_image(image_file):
        # Read file as bytes and encode to base64
        return base64.b64encode(image_file.read()).decode('utf-8')

    # Function to convert image to text using LLaVA
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

    # Function to generate test instructions based on image description
    def generate_test_instructions(client, image_description):
        detailed_prompt = (
            "You are a QA tester. Based on the description provided, write a detailed test case for the digital product feature. "
            "Include the following sections:\n\n"
            "1. **Description**: Briefly describe what the test case is about.\n"
            "2. **Pre-conditions**: List all the pre-conditions that need to be set up or ensured before testing.\n"
            "3. **Testing Steps**: Provide clear, step-by-step instructions on how to perform the test.\n"
            "4. **Expected Result**: Describe what should happen if the feature works correctly.\n\n"
            "Use clear and concise language to ensure the test case can be easily followed by any QA tester."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": detailed_prompt,
                },
                {
                    "role": "user",
                    "content": image_description,
                }
            ],
            model=llama31_model
        )
        return chat_completion.choices[0].message.content

    # Streamlit UI
    st.title("Automated Testing Instructions Generator")

    # Text box for optional context
    context = st.text_input("Enter any additional context (optional)")

    # Multi-image uploader
    uploaded_images = st.file_uploader("Upload Screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # Button to trigger description generation
    if st.button("Describe Testing Instructions") and uploaded_images:
        st.write("Generating testing instructions...")

        # Process images and generate testing instructions
        testing_instructions = []
        for image_file in uploaded_images:
            # Encode image to base64
            base64_image = encode_image(image_file)

            # Generate image description using LLaVA
            prompt = "Describe this image in detail for testing purposes."
            image_description = image_to_text(client, llava_model, base64_image, prompt)

            # Generate test instructions from image description
            test_instructions = generate_test_instructions(client, image_description)
            testing_instructions.append(test_instructions)

        # Display testing instructions
        for i, instruction in enumerate(testing_instructions):
            st.write(f"### Test Case {i+1}")
            st.write(instruction)
    else:
        st.info("Please upload at least one screenshot to generate testing instructions.")
