from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini model and get responses

model = genai.GenerativeModel("gemini-3.6-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

## Initialize Streamlit app
st.set_page_config(page_title="Q&A with Gemini")

st.header("Gemini Application")
input = st.text_input("Input: ", key="input")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("Tell me about the image")

## if submit is clicked

if submit:
    if uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        response = get_gemini_response(input, image)
        st.subheader("Response:")
        st.write(response)