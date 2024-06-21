import os
from dotenv import load_dotenv
import google.generativeai as genai

# Function to generate content based on a course input
def generate_course_quiz(course):
    # Load environment variables if needed
    load_dotenv()

    # Configure the generative AI model
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings if needed
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    # Prompt to generate a detailed roadmap for the specified course
    prompt = [
        f"generate a profession quiz of 10 questions with 4 options based on {course} and also include codding snippet questions. level of difficulty should be medium. and generate in json format like in key value pair with 4 keys (id, question, option , answer)."
    ]

    # Generate content based on the prompt
    response = model.generate_content(prompt)

    # Extract the generated text from the response
    quiz = response.text

    return quiz
