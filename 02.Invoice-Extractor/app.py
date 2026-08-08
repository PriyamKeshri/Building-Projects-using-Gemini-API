from dotenv import load_dotenv

load_dotenv()  # Load all environment variables from .env file

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

### Function to load Gemini
model = genai.GenerativeModel("gemini-3.6-flash")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded. Please upload an invoice image.")

## Initializing the Streamlit app
st.set_page_config(page_title="Invoice Extractor", page_icon=":money_with_wings:", layout="wide")
st.header("Multilangual Invoice Extractor")
input = st.text_input("Input prompt: ", key = "input")
uploaded_file = st.file_uploader("Upload an invoice image..", type=["png", "jpg", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("Tell me the invoice details")

input_prompt = """"
You are an expert in understanding invoices. We will upload an
invoice image and you will have to answer any questions related
to the invoice. You will have to extract the details from the
invoice image and answer the questions in a structured format.
"""

# If submit button is clicked
if submit: 
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input )
    st.subheader("Response:")
    st.write(response)