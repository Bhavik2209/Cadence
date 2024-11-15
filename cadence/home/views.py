from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegForm, UserLoginForm
from django.contrib.auth import logout
from datetime import datetime
from django.http import JsonResponse
import json
import pyrebase
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .roadmap.quiz import generate_course_quiz
from .roadmap.app import generate_course_roadmap
from .habits.app import generate_daily_timetable
import re
import json
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import os

load_dotenv()
config = {
    "databaseURL": os.getenv("databaseURL"),
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId":  os.getenv("appId"),
    "measurementId": os.getenv("databaseURL")
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.

 
def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def quiz_view(request):
    if request.method == "POST":
        print("quiz requested")
        course_name = request.POST.get('course_name')
        print(course_name)
        # Your logic to handle the course name and generate the quiz
        questions_anwers, answer_key = generate_course_quiz(course_name)
        # print("answer key:", answer_key)
        return render(request, 'quiz.html', {'questions': questions_anwers, 'answer_key': json.dumps(answer_key)})
    print("not getting post request")


def signup(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Ensure you're using the correct field name
            password = form.cleaned_data['password1']
            print(email,password)
            try:
                # creating a user with the given email and password
                user = authe.create_user_with_email_and_password(
                    email, password)
                uid = user['localId']
                request.session['uid'] = uid
                messages.success(request, 'Account created successfully.')
                print("created")
                # Redirect to login page after successful signup
                return redirect('user_login')

            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return render(request, "signup.html", {'form': form})
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UserRegForm()

    return render(request, 'signup.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        print("Form submitted")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authe.sign_in_with_email_and_password(email, password)
                session_id = user['idToken']
                request.session['uid'] = user['localId']  # Store localId
                request.session['user'] = user

                request.session['email'] = email

                messages.success(request, 'Login successful.')
                print("Login successful")
                return redirect('index')
            except Exception as e:
                message = f"Invalid Credentials! Please check your data. Error: {str(e)}"
                print("Login failed: ", message)
                messages.error(request, message)
                return render(request, "login.html", {"form": form})
            except:
                message = "Invalid Credentials!! Please check your data."
                return render(request, "login.html", {"message": message, "form": form})

        else:
            print("Form is invalid")
            print("Form errors: ", form.errors)
            messages.error(request, 'Invalid form data')
            return render(request, 'login.html', {'form': form})
    else:

        form = UserLoginForm()
        print("GET request")

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    # Remove any other session variables related to authentication
    request.session.pop('uid', None)
    request.session.pop('user', None)
    return redirect('index')


def products(request):
    return render(request, 'product.html')


def path_pro(request):
    zipped_roadmap =[]
    if request.method == "POST":
        course = request.POST.get('goal')
        if course:  # Check if the course input is not empty
            request.session['course'] = course
            roadmap = generate_course_roadmap(course)
            print(roadmap)
            zipped_topics  = list(zip(roadmap["topics"], roadmap["subtopics"]))

        
            zipped_roadmap = {
                'zipped_topics': zipped_topics
            }
            print(zipped_roadmap)
            # Store roadmap_html in session
            request.session['roadmap_data'] = zipped_topics
        else:
            messages.error(request, "Please enter a valid goal.")

    return render(request, 'path_pro.html', {'roadmap': zipped_roadmap})


def save_roadmap(request):
    if request.method == 'POST':
        user_email = request.session.get('email')  # Use email
        course = request.session.get('course')
        if user_email:
            data = json.loads(request.body)
            roadmap = request.session.get('roadmap_data')

            if roadmap:
                new_roadmap = {
                    "user_email": user_email,
                    "course": course,
                    "roadmap": roadmap,
                    "completed": False
                }
                database.child("roadmaps").push(new_roadmap)
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "error": "No roadmap content"})
        return JsonResponse({"success": False, "error": "User not authenticated"})
    return JsonResponse({"success": False, "error": "Invalid request"})


def time_track(request):
    return render(request, 'time_track.html')

    #     form = UserLoginForm()  # Create a new form instance for GET requests

    # return render(request, 'login.html', {'form': form})


def convert_to_html(input_text):
    # Split the input text into sections
    sections = input_text.split('\n\n')

    # Initialize HTML content
    html_output = ""

    # Iterate over each section to build the HTML
    for section in sections:
        # Skip empty sections
        if not section.strip():
            continue

        # Handle headers
        if section.startswith("**"):
            header = section.strip("**").strip()
            html_output += f'<h3>{header}</h3>'

        # Handle lists
        elif section.startswith("* "):
            html_output += '<ul>'
            items = section.split('\n')
            for item in items:
                if item.startswith("* "):
                    item_content = item.lstrip("* ").strip()
                    html_output += f'<li>{item_content}</li>'
            html_output += '</ul>'

        # Handle nested lists (like timetable)
        elif section.startswith("**Time Table:**"):
            timetable_html = '<h3>Time Table</h3>'
            lines = section.split('\n')[1:]  # Skip the **Time Table:** line
            for line in lines:
                if line.startswith("**"):
                    if "timetable-item" in locals():
                        timetable_html += timetable_item
                    time = line.strip("**").strip()
                    timetable_item = f'<div class="timetable-item"><strong>{time}</strong><ul>'
                elif line.startswith("* "):
                    activity = line.lstrip("* ").strip()
                    timetable_item += f'<li>{activity}</li>'
            if "timetable-item" in locals():
                timetable_html += timetable_item + '</ul></div>'
            html_output += timetable_html

    return html_output


def habits_pro(request):
    answers = ''
    time_table = ''
    if request.method == 'POST':
        priority_1 = request.POST.get('priority_1')
        commitments = request.POST.get('commitments')
        sleep_schedule = request.POST.get('sleep_schedule')
        time_allocation = request.POST.get('time_allocation')
        productivity_hours = request.POST.get('productivity_hours')
        daily_goals = request.POST.get('daily_goals')
        day_structure = request.POST.get('day_structure')
        break_preferences = request.POST.get('break_preferences')
        existing_habits = request.POST.get('existing_habits')
        different_days = request.POST.get('different_days')

        three_prio = priority_1.split(",")

        # User email (assuming it's stored in session)
        user_email = request.session.get('email', 'default_email@example.com')
        print(user_email)
        # Save each priority in three_prio separately to Firebase
        for priority in three_prio:
            data = {
                'user_email': user_email,
                'priority': priority.strip(),  # assuming priority might have leading/trailing spaces
                'completed': False,  # Assuming this is a new entry and not yet completed
                'date': datetime.now().isoformat(),
                
            }

            # Push data to Firebase
            database.child('user_priorities').push(data)

        # Generate timetable and convert to HTML
        answers = generate_daily_timetable([priority_1, commitments, sleep_schedule, time_allocation,
                                            productivity_hours, daily_goals, day_structure, break_preferences,
                                            existing_habits, different_days])
        time_table = convert_to_html(answers)

        return render(request, 'habitspro.html', {'time_table': time_table})
    else:
        return render(request, 'habitspro.html')


def generate_roadmap_html(roadmap_text):
    # Break the text into lines
    lines = roadmap_text.split('\n')

    # Initialize an empty HTML string and a flag for list items
    html = ""
    in_list = False
    last_level = 0

    # Function to close the list tags based on the current and last level
    def close_lists(current_level):
        nonlocal html, in_list, last_level
        while last_level >= current_level:
            html += "</ul>"
            last_level -= 1
        in_list = False

    # Loop through each line and convert to HTML
    for line in lines:
        # Remove unwanted prefixes
        line = line.lstrip('-#* ').strip()
        # Phase headers
        if line.startswith("**") and line.endswith("**"):
            close_lists(0)
            html += f"<h2 style='font-size: 2em; margin-bottom: 10px;'>{line.strip('**').strip()}</h2>"
        # Main topics (subheaders)
        elif line.startswith("Phase") and line.endswith("**"):
            close_lists(1)
            html += f"<h3 style='font-size: 1.75em; margin-bottom: 8px;'>{line.strip('**').strip()}<input type='checkbox' style='float: right; margin-right: 10px; width: 20px; height: 20px;'></h3>"
            last_level = 1
        # Sub-subheaders
        elif line.startswith("*") and line.endswith(":"):
            close_lists(2)
            html += f"<h4 style='font-size: 1.5em; margin-bottom: 6px;'>{line.strip('*:').strip()}</h4>"
            last_level = 2
        # List items
        elif line.startswith("*"):
            if not in_list:
                html += "<ul>"
                in_list = True
            html += f"<li style='margin-bottom: 4px;'>{line.strip('*').strip()}</li>"
        else:
            close_lists(0)
            html += f"<p>{line.strip()}</p>"

    close_lists(0)

    # Wrap the HTML in a div
    html = f"<div class='roadmap'>{html}</div>"

    return html


def my_roadmaps(request):
    user_email = request.session.get('email')  # Use email
    print(f"Fetching roadmaps for user_email: {user_email}")  # Debugging line
    if user_email:
        roadmaps = database.child("roadmaps").order_by_child("user_email").equal_to(user_email).get().val()
        print(f"Fetched roadmaps: {roadmaps}")  # Debugging line
        if roadmaps:
            roadmaps_list = [(key, value) for key, value in roadmaps.items()]
            for key, roadmap in roadmaps_list:
                roadmap['roadmap_html'] = generate_roadmap_html(
                    roadmap['roadmap'])
        else:
            roadmaps_list = []

        badges = []  # Replace with your logic to get user badges

        return render(request, 'my_roadmaps.html', {'roadmaps': roadmaps_list, 'badges': badges})
    else:
        messages.error(request, "User not authenticated. Please log in.")
        return redirect('user_login')


@csrf_exempt
def habits(request):

    return render(request, 'habits.html')

@csrf_exempt
def submit_priorities(request):
    if request.method == 'POST':
        user_email = request.session['email']
        priorities = request.POST.get('priorities[]')
        completed = request.POST.get('completed[]')
        priorities =json.loads(priorities)
        completed = json.loads(completed)
        print(user_email)
        print(priorities)
        print(completed)  
        for i, priority in enumerate(priorities):
            data = {
                'user_email': user_email,
                'priority': priority,
                'completed': completed[i] == True,
                'date': datetime.now().isoformat()
            }
            database.child("user_priorities").push(data)

        return JsonResponse({'status': 'success'})


def get_priorities_data(request):
    user_email = request.session['email']  # Assuming you can get the user ID from the request
    print(user_email)
    user_priorities = database.child("user_priorities").order_by_child("user_email").equal_to(user_email).get()
    priorities_data = [habit.val() for habit in user_priorities.each()] if user_priorities.each() else []
    # priorities_data= [{'is_completed': False, 'priority': 'exercise', 'timestamp': '2024-11-14T15:17:44.881603', 'user_email': 'hellohello@gmail.com'}, {'is_completed': False, 'priority': 'coding', 'timestamp': '2024-11-14T15:17:44.942235', 'user_email': 'hellohello@gmail.com'}, {'is_completed': False, 'priority': 'familytime', 'timestamp': '2024-11-14T15:17:44.990835', 'user_email': 'hellohello@gmail.com'}]
    print(priorities_data)

    if priorities_data:
        return JsonResponse({'data': priorities_data})
    else:
        return JsonResponse({'data': []})
    
