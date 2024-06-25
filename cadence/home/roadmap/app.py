import os
from dotenv import load_dotenv
import google.generativeai as genai

# Function to generate content based on a course input
def generate_course_roadmap(course):
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
        f"Generate a detailed and comprehensive {course} roadmap and make sure the roadmap is realistic and includes all the topics with basics. The roadmap should contain only basic topics and just list out its applications at the end. Ensure that content is original, informative, and maintains a consistent throughput. The roadmap must be detailed."
    ]

    # Generate content based on the prompt
    response = model.generate_content(prompt)

    # Extract the generated text from the response
    res = response.text

    return res

