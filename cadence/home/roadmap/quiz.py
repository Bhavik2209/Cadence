import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
from django.utils.safestring import mark_safe
import json

def generate_course_quiz(course):
    load_dotenv()
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
    )

    prompt = [
        f'''Generate a professional quiz with only theory questions, without giving any programming questions. Generate 10 questions with 4 options each based on {course}.
        Give the results in the form of an array of objects like this. Don't add any other text before or after the output:
        {{
            "question_name":"",
            "options" : ["option1", "option2" , "option3" , "option4"],
            "correct_option_number" :  "",
        }}
        only give the correct option number dont give the whole answre

        '''
    ] 

    # response = model.generate_content(prompt)
    # res = response.text
    # questions_str = res.replace('```json', '').replace('```', '').strip()
    
    # # Convert JSON string to list of questions 
    # try:
    #     questions_anwers = json.loads(questions_str)
    # except json.JSONDecodeError: 
    #     return json.JSONDecodeError
    

    questions_anwers = [{'question_name': 'Which of the following is a data type in TypeScript?', 'options': ['number', 'string', 'boolean', 'all of the above'], 'correct_option_number': 4} ,
                        {'question_name': 'Which of the following is a key difference between TypeScript and JavaScript?', 'options': ['TypeScript is a statically typed language, while JavaScript is a dynamically typed language.', 'TypeScript compiles to JavaScript, while JavaScript is interpreted.', 'TypeScript supports object-oriented programming, while JavaScript does not.', 'TypeScript is a newer language than JavaScript.'], 'correct_option_number': 1},
                        {'question_name': 'Which of the following is a key difference between TypeScript and JavaScript?', 'options': ['TypeScript is a statically typed language, while JavaScript is a dynamically typed language.', 'TypeScript compiles to JavaScript, while JavaScript is interpreted.', 'TypeScript supports object-oriented programming, while JavaScript does not.', 'TypeScript is a newer language than JavaScript.'], 'correct_option_number': 1},]


    correct_answers = []
    for ques in questions_anwers:
        correct_answers.append(ques['correct_option_number'])

    print(questions_anwers[0])
    print(correct_answers)
    return questions_anwers,correct_answers
