import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
# Function to generate content based on a course input
def generate_daily_timetable(answers):
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
        f'''
        these are some questions for generating daily routine time table : 
        What are your top 3 priorities for the day? (e.g., work, study, exercise, family time, creative projects)
        Do you have any fixed commitments? (e.g., work hours, meetings, appointments)
        What time do you typically wake up and go to bed? (This will help determine the overall length of your day)
        How much time do you want to dedicate to each priority? (This can be flexible, but having an idea will help us build a balanced schedule)
        Are you a morning person, evening person, or somewhere in between? (This will help us allocate time for your most productive hours)
        Do you have any specific goals you want to achieve during the day? (e.g., finish a project, learn a new skill, read a certain number of pages)
        Do you prefer to have your day structured or more flexible? (This will influence how detailed the timetable is)
        What are your ideal breaks like? (e.g., short walks, meditation, listening to music)
        Do you have any existing habits or routines you'd like to incorporate? (e.g., daily exercise, journaling, reading)
        Are there any specific days that are different from your usual routine? (e.g., weekends, holidays).
        and these are the answers of these 10 questions {answers}. based on this questions and answers create a complete and realistic time table for me.
        Give the response in a json, formatted like this:
        {{
            "time_slot" : 
            "activity" :
        }}
        '''
    ]

    # Generate content based on the prompt
    response = model.generate_content(prompt)

    # Extract the generated text from the response
    res = response.text
    res =res.replace('```json', '').replace('```', '').strip()
    # Convert JSON string to list of questions 
    try:
        timetable = json.loads(res)
        print(timetable)
        return timetable
    except json.JSONDecodeError: 
<<<<<<< HEAD
        return json.JSONDecodeError
=======
        return json.JSONDecodeError

>>>>>>> 7df6fe4436564d3da2f6d23de3b169cb042e1d6e
