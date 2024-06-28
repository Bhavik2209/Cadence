import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
from django.utils.safestring import mark_safe



def convert_text_to_html(text):
    html_output = ""
    # Split the input text to separate questions from the answer key
    parts = text.strip().split("*Answer Key:*")
    questions = parts[0].strip().split("\n\n")
    answers = parts[1].strip().split("|")

    pattern = re.compile(r'[^a-dA-D]')

    for i, question_block in enumerate(questions):
        lines = question_block.strip().split("\n")
        question_text = lines[0].strip().strip("*")  # Remove leading/trailing spaces and asterisks
        options = lines[1:]
        if question_text == "Answer Key:":
            continue
        html_output += f'<div class="question-card">'
        html_output += f'<h3 class="question-title">{question_text}</h3>'
        html_output += f'<div class="options">'

        opvalue = ['a', 'b', 'c', 'd']
        for j, option in enumerate(options):
            option_id = f"q{i}{j+1}"
            option_text = option.strip()
            html_output += f'<input type="radio" name="q{i}" value="{opvalue[j]}" id="{option_id}" />'
            html_output += f'<label for="{option_id}" class="option-button">{option_text}</label><br>'

        html_output += f'</div></div>'

    answers = [pattern.sub('', answer).lower() for answer in answers]  # Clean the answer key and convert to lower case

    return mark_safe(html_output), answers


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
        f"Generate a professional quiz with only theory questions, without giving any programming questions. Generate 10 questions with 4 options each based on {course}. The level of difficulty should be medium. Provide the answer key with answers separated by a delimiter '|'."
    ]

    response = model.generate_content(prompt)
    res = response.text
    quiz_html, answers = convert_text_to_html(res)

    return quiz_html, answers
