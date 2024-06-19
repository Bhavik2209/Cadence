from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

##initialize our streamlit app

st.title("Roadmap AI")
st.subheader("Welcome")

with st.sidebar:
    st.title("Input")
    st.write("You can click on Create button multiple times to generate a perfect roadmap")
    course = st.text_input("topic")
    

    

    prompt = [
        f"generate a detailed and comprehensive {course} roadmap and make sure roadmap is realistic and include all the topics with basics. roadmap should contain only basic topics and just list out its applications at the end. Ensure that content is original, informative and maintain a consistent throughput. roadmap must be detailed"
    ]

    response = model.generate_content(prompt)
    submit_button = st.button("Create")

if submit_button:
    st.write(response.text)
