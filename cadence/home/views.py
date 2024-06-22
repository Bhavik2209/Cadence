from django.shortcuts import render,redirect
from .forms import UserRegForm,UserLoginForm

import pyrebase
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

config = {
    "apiKey": "${API_KEY}",
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
                return redirect('login')  # Redirect to login page after successful signup
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return render(request, "signup.html", {'form': form})
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UserRegForm()

    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
        # if there is no error then signin the user with given email and password
                user=authe.sign_in_with_email_and_password(email,password)
            except:
                message="Invalid Credentials!!Please ChecK your Data"
                return render(request,"Login.html",{"message":message})
            session_id=user['idToken']
            request.session['uid']=str(session_id)
            return render(request,"index.html")
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UserLoginForm()  # Create a new form instance for GET requests
    
    return render(request, 'login.html', {'form': form})