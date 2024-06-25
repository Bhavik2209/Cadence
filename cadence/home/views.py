from django.shortcuts import render,redirect
from .forms import UserRegForm,UserLoginForm
from django.contrib.auth import logout

import pyrebase
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .roadmap.quiz import generate_course_quiz

from .roadmap.app import generate_course_roadmap
import re

config = {
  "apiKey": "AIzaSyClUwHrnTgllI4tAawe2rTY4luuYbzbuFo",
  "authDomain": "test-6ef0b.firebaseapp.com",
  "databaseURL": "https://test-6ef0b-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "test-6ef0b",
  "storageBucket": "test-6ef0b.appspot.com",
  "messagingSenderId": "595401935708",
  "appId": "1:595401935708:web:a0ee6c32a345713f930f99",
  "measurementId": "G-ZLCG76PVW3"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def index(request):
    return render(request,"index.html")

def quiz_view(request):
    course = "Python"
    quiz_html, answer_key = generate_course_quiz(course)
    return render(request, 'quiz.html', {'quiz_html': quiz_html, 'answer_key': answer_key})

def signup(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']  # Ensure you're using the correct field name
            try:
                # creating a user with the given email and password
                user = authe.create_user_with_email_and_password(email, password)
                uid = user['localId']
                request.session['uid'] = uid
                messages.success(request, 'Account created successfully.')

                return redirect('login') # Redirect to login page after successful signup

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
                request.session['uid'] = str(session_id)

                request.session['user'] = user
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
    request.session.pop('uid', None)  # Remove any other session variables related to authentication
    request.session.pop('user', None)
    return redirect('index')

def products(request):
    return render(request,'product.html')


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
        # Subheaders
        elif line.startswith("Phase") and line.endswith("**"):
            close_lists(1)
            html += f"<h3 style='font-size: 1.75em; margin-bottom: 8px;'>{line.strip('**').strip()}<input type='checkbox' style='float: right; margin-right: 10px;'></h3>"
            last_level = 1
        # Sub-subheaders
        elif line.startswith("*") and line.endswith(":"):
            close_lists(2)
            html += f"<h4 style='font-size: 1.5em; margin-bottom: 6px;'>{line.strip('*:').strip()}<input type='checkbox' style='float: right; margin-right: 10px;'></h4>"
            last_level = 2
        # List items
        elif line.startswith("*"):
            if not in_list:
                html += "<ul>"
                in_list = True
            html += f"<li style='margin-bottom: 4px;'>{line.strip('*').strip()}<input type='checkbox' style='float: right; margin-right: 10px;'></li>"
        else:
            close_lists(0)
            html += f"<p>{line.strip()}</p>"
    
    close_lists(0)
    
    # Wrap the HTML in a div
    html = f"<div class='roadmap'>{html}</div>"
    
    return html

def path_pro(request):
    roadmap_html = None
    if request.method == "POST":
        course = request.POST.get('goal')
        if course:  # Check if the course input is not empty
            roadmap = generate_course_roadmap(course)
            roadmap_html = generate_roadmap_html(roadmap)
            # roadmap_html = roadmap
    return render(request, 'path_pro.html', {'roadmap_html': roadmap_html})

def time_track(request):
    return render(request,'time_track.html')

    #     form = UserLoginForm()  # Create a new form instance for GET requests

    # return render(request, 'login.html', {'form': form})