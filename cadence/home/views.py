from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegForm, UserLoginForm
from django.contrib.auth import logout
from datetime import date
from django.http import JsonResponse
import json
import pyrebase
from django.contrib import messages
from .roadmap.quiz import generate_course_quiz
from .roadmap.app import generate_course_roadmap
from .habits.app import generate_daily_timetable
import json
from dotenv import load_dotenv
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
        if 'quiz_submission' in request.POST:
            # Handle quiz submission
            course_name = request.POST.get('course_name')
            marks = float(request.POST.get('marks', 0))
            user_email = request.session.get('email')

            if user_email:
                try:
                    # Get all roadmaps for the current user
                    roadmaps = database.child("roadmaps").get()
                    
                    if roadmaps:
                        for roadmap in roadmaps.each():
                            roadmap_data = roadmap.val()
                            # Check if this is the correct roadmap (matching user and course)
                            if (roadmap_data.get('user_email') == user_email and 
                                roadmap_data.get('course') == course_name):
                                
                                if marks >= 7:
                                    # Update the completed status in Firebase
                                    database.child("roadmaps").child(roadmap.key()).update({
                                        "completed": True
                                    })
                                    messages.success(request, f'Congratulations! You have completed the {course_name} roadmap!')
                                else:
                                    messages.warning(request, 'You need to score at least 7 marks to complete this roadmap.')
                                break
                    
                    return redirect('my_roadmaps')
                
                except Exception as e:
                    print(f"Error updating roadmap: {str(e)}")
                    messages.error(request, 'An error occurred while updating your progress.')
                    return redirect('my_roadmaps')
            else:
                messages.error(request, 'User not authenticated')
                return redirect('login')  # or wherever you want to redirect unauthenticated users
        else:
            # Your existing quiz generation code
            print("quiz requested")
            course_name = request.POST.get('course_name')
            questions_anwers, answer_key = generate_course_quiz(course_name)
            return render(request, 'quiz.html', {
                'questions': questions_anwers, 
                'answer_key': json.dumps(answer_key),
                'course_name': course_name
            })
    
    return redirect('my_roadmaps')

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
                print("created")
                return redirect('user_login') # Redirect to login page after successful signup

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


def habits_pro(request):
    answers = ''
    time_table = ''
    if request.method == 'POST':
        priorities = request.POST.get('priorities')
        commitments = request.POST.get('commitments')
        sleep_schedule = request.POST.get('sleep_schedule')
        time_allocation = request.POST.get('time_allocation')
        productivity_hours = request.POST.get('productivity_hours')
        daily_goals = request.POST.get('daily_goals')
        day_structure = request.POST.get('day_structure')
        break_preferences = request.POST.get('break_preferences')
        existing_habits = request.POST.get('existing_habits')
        different_days = request.POST.get('different_days')

        #getting each priority
        three_prio = priorities.split(",")
        
        # User email (assuming it's stored in session)
        user_email = request.session.get('email', 'default_email@example.com')
        print(user_email)
        priorities_list=[]
        completed_list=[]
        count_list=[]

        for priority in three_prio: 
            priorities_list.append(priority.strip())
            completed_list.append(False)
            count_list.append(0)

        data = {
            'user_email': user_email,
            'priority': priorities_list,  
            'completed': completed_list,  
            'count':count_list,
            'date': date.today().isoformat(),
        }
        #checking if there is data in session if it exists then updaet it in db
        try:
            priorities_data=request.session['priorities_data']
            print(priorities_data) 
            user_priorities = database.child("user_priorities").order_by_child("user_email").equal_to(user_email).get()
            if user_priorities:
                print("priorities_data exist")
                for item in user_priorities.each():  # Loop through each record for the user
                    database.child("user_priorities").child(item.key()).update({
                        "priority":priorities_list,
                        "completed": completed_list, 
                        'count':count_list,
                        "date": date.today().isoformat()
                    })

        #if not then push it to db
        except:

            print("pushing data-",data)

            database.child('user_priorities').push(data)

        # Generate timetable and convert to HTML

        answers = generate_daily_timetable([priorities, commitments, sleep_schedule, time_allocation,
                                            productivity_hours, daily_goals, day_structure, break_preferences,
                                            existing_habits, different_days])

        print(answers)
        request.session['priorities_data'] =[data]  
        return render(request, 'habitspro.html', {'time_table': answers})
    else:
        return render(request, 'habitspro.html')

def my_roadmaps(request):
    user_email = request.session.get('email')
    if user_email:
        roadmaps = database.child("roadmaps").order_by_child("user_email").equal_to(user_email).get().val()
        if roadmaps:
            roadmaps_list = [(key, value) for key, value in roadmaps.items()]
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
        completed_priorities = json.loads(request.POST.get('priorities[]'))  # List of priorities ticked by the user
        priorities_data = request.session.get('priorities_data')  # Fetch the existing priorities data
        priorities_data = priorities_data[0]  # Assuming only one set of priorities is returned

        print("User Email:", user_email)
        print("Completed Priorities:", completed_priorities)

        # Iterate over priorities and update the `completed` field
        for i, priority in enumerate(priorities_data['priority']):
            if priority in completed_priorities:
                priorities_data['completed'][i] = True  # Mark as completed
                priorities_data['count'][i] +=1        # increase the count by 1

        print(priorities_data) 
        # Query Firebase for the user's data and update it
        user_priorities = database.child("user_priorities").order_by_child("user_email").equal_to(user_email).get()

        for item in user_priorities.each():  # Loop through each record for the user
            database.child("user_priorities").child(item.key()).update({
                "completed": priorities_data["completed"],
                'count':priorities_data["count"],
                "date": date.today().isoformat()
            })
        # Optionally, update the session with the modified `priorities_data`
        request.session['priorities_data'] = [priorities_data]

        print("Updated Priorities Data:", priorities_data)

        # Return success response
        return JsonResponse({'status': 'success', 'updated_priorities': priorities_data})


def get_priorities_data(request):
    user_email = request.session['email']  # Assuming you can get the user ID from the request
    print(user_email)

    #getting data froms session
    try:
        priorities_data=request.session['priorities_data']
    #if not then fetch it from db
    except:
        print("fetching data from db")
        user_priorities = database.child("user_priorities").order_by_child("user_email").equal_to(user_email).get()
        priorities_data = [habit.val() for habit in user_priorities.each()] if user_priorities.each else []

    print(" priorities_data" ,priorities_data)
    #so if the completed is set to true , check if the date is today's date and if it is than do nothing , and if the day is not same then change the completed to false so to show the priorities again.
    for prior in priorities_data:
        for i, comple in enumerate(prior['completed']):
            if (comple==True) and (prior['date'] != date.today().isoformat()):
                prior['completed'][i]=False
             
    print("updated priorities_data" ,priorities_data)

    #example data
    # priorities_data=[{'completed': [True, True, True], 'count': [1, 1, 1], 'date': '2024-11-18', 'priority': ['coding', 'familytime', 'swimming'], 'user_email': 'hellohello@gmail.com'}]
    
    if priorities_data:
        request.session['priorities_data'] =priorities_data 
        return JsonResponse({'data': priorities_data})
    else:
        return JsonResponse({'data': []})
    
