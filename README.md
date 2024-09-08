# FeatureTestify (Automated Testing Instructions Generator)

This project is a web application that uses a multimodal LLM (LLaVA and LLaMA) via the Groq API to generate detailed testing instructions for any digital product's features based on screenshots. The application is built with Streamlit for the front end, providing an easy-to-use interface for uploading images and receiving step-by-step test cases. FeatureTestify converts your product screenshots into structured testing scenarios, complete with pre-conditions, steps, and expected results.

## Features

- **Image Upload**: Upload multiple screenshots of a digital product's features.
- **Contextual Input**: Optionally provide additional context for generating more accurate test instructions.
- **Automated Test Case Generation**: Automatically generate detailed test instructions, including:
  - **Description**: What the test case is about.
  - **Pre-conditions**: What needs to be set up or ensured before testing.
  - **Testing Steps**: Clear, step-by-step instructions on how to perform the test.
  - **Expected Result**: What should happen if the feature works correctly.
  
## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [Groq API](https://groq.com/) using:
  - **LLaVA** for image description.
  - **LLaMA** for generating testing instructions based on the image descriptions.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Streamlit](https://streamlit.io/)
- [Groq API Key](https://groq.com/) (Sign up and create an account to obtain your API key)
- [Pillow (PIL)](https://pillow.readthedocs.io/) for image processing

### Usage

- Open the web app in your browser.
- Enter any additional context in the text box (optional).
- Upload one or more screenshots of the digital product's features.
- Click on the "Describe Testing Instructions" button.
- View the generated testing instructions displayed below.


### Example 
To demonstrate the tool's capabilities, we use features from the Red Bus mobile app such as:

- Source, Destination, and Date Selection
- Bus Selection
- Seat Selection
- Pick-up and Drop-off Point Selection
- Offers
- Filters
- Bus Information

## Troubleshooting
- Ensure your Groq API key is correctly set in the .env file.
- Verify that all dependencies are installed.
- Check if Streamlit and Python are properly installed and set up.