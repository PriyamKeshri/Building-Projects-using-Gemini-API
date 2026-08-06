from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini model and get responses

model = genai.GenerativeModel("gemini-3.6-flash")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

## Initialize Streamlit app

st.set_page_config(page_title="Q&A with Gemini")

st.header("Gemini Application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask a question")

## When submit is clicked

if submit:
    response = get_gemini_response(input)
    st.subheader("Response:")
    st.write(response)