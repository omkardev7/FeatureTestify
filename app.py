import streamlit as st
from dotenv import load_dotenv
import warnings
import os
from groq import Groq
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from textwrap import wrap

st.set_page_config(
    page_title="FeatureTestify",
    page_icon="🖥️",
    layout="centered",
    initial_sidebar_state="auto",
)

# Load environment variables
load_dotenv()

# Retrieve the API key from the environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY is not set. Please set the API key in your environment variables.")
else:
    # Initialize Groq API client with the API key
    client = Groq(api_key=groq_api_key)
    vision_model = 'meta-llama/llama-4-scout-17b-16e-instruct'
    text_model = 'llama-3.1-8b-instant'

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
            "5. **Suggestions**: Give suggestions for any additional test scenarios or improvements.\n\n"
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
            model=text_model
        )
        return chat_completion.choices[0].message.content
    
    def create_pdf(testing_instructions):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        margin_x = 72  # Left margin
        line_height = 14  # Line height for regular text
        y_position = height - 72  # Starting position from the top

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(margin_x, y_position, "Generated Testing Instructions")
        y_position -= 30

        # Loop through each test case and format accordingly
        for i, instruction in enumerate(testing_instructions):
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(margin_x, y_position, f"Test Case {i + 1}")
            y_position -= 20

            # Split the instruction into sections
            sections = instruction.split("\n\n")
            
            for section in sections:
                # Determine if section starts with a header (e.g., **Description:**) and format appropriately
                if section.startswith("**"):
                    header, text = section.split("**", 2)[1:]  # Split off the header and content
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(margin_x, y_position, header.strip(":"))
                    y_position -= 16

                    # Wrap and print the remaining text in the section
                    pdf.setFont("Helvetica", 11)
                    wrapped_text = wrap(text.strip(), 80)  # Wrap text at 80 characters
                    for line in wrapped_text:
                        pdf.drawString(margin_x + 10, y_position, line)  # Indent wrapped text
                        y_position -= line_height
                else:
                    # General text with potential bullet points or numbers
                    wrapped_text = wrap(section.strip(), 90)
                    pdf.setFont("Helvetica", 11)
                    for line in wrapped_text:
                        pdf.drawString(margin_x + 10, y_position, line)
                        y_position -= line_height

                y_position -= 10  # Extra space after each section

                # Start a new page if the y_position goes below the margin
                if y_position < 72:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 11)
                    y_position = height - 72

        pdf.save()
        buffer.seek(0)
        return buffer

    # Streamlit UI
    st.title("FeatureTestify")
    st.subheader("(Automated Testing Instructions Generator)")

    # Text box for optional context
    context = st.text_input("Enter any additional context (optional)")

    # Multi-image uploader
    uploaded_images = st.file_uploader("Upload Screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    testing_instructions = []

    # Button to trigger description generation
    if st.button("Describe Testing Instructions") and uploaded_images:
        st.write("Generating testing instructions...")

        # Process images and generate testing instructions
        
        for image_file in uploaded_images:
            # Encode image to base64
            base64_image = encode_image(image_file)

            # Generate image description using LLaVA
            prompt = "Describe this image in detail for testing purposes."
            image_description = image_to_text(client, vision_model, base64_image, prompt)

            # Generate test instructions from image description
            test_instructions = generate_test_instructions(client, image_description)
            testing_instructions.append(test_instructions)

        # Display testing instructions
        for i, instruction in enumerate(testing_instructions):
            st.write(f"### Test Case {i+1}")
            st.write(instruction)
    else:
        st.info("Please upload at least one screenshot to generate testing instructions.")
        
        # New Button to Download the Instructions as PDF
    if testing_instructions:
        pdf_buffer = create_pdf(testing_instructions)
        st.write("### Download your instructions as a PDF")
        st.download_button(
            label="Download Testing Instructions PDF",
            data=pdf_buffer,
            file_name="testing_instructions.pdf",
            mime="application/pdf"
        )
        
    
