from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input,input_prompt])
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Roadmap generator")

st.header("Roadmap generator")
input = st.text_input("what do you want to learn")  

submit=st.button("Roadmap")

input_prompt = """
               f"Given the user-specified topic {input} , create a comprehensive, and 
               structured learning roadmap. roadmap should be topics specified. 
               This roadmap should cover fundamental concepts and advanced techniques 
               related to. For example. It should progress to more advanced topics. Ensure that each topic logically builds 
               on the previous one, providing a clear and achievable pathway for learning 
               and skill development. At the end of the roadmap, include a segment discussing 
               practical applications or real-world use cases, demonstrating how the language 
               concepts learned can be applied in various domains."
               """


if submit:
    response=get_gemini_response(input,input_prompt)
    st.subheader("The Response is")
    st.write(response)





