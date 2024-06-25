from django.shortcuts import render,redirect
from .forms import UserRegForm,UserLoginForm
from django.contrib.auth import logout

import pyrebase
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ..roadmap.quiz import generate_course_quiz
config = {
  "apiKey": "${api_key}",

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



