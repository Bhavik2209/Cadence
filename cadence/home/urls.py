from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.user_login,name='user_login'),
    path("signup/",views.signup,name='signup'),
    path('logout/', views.logout_user, name='logout_user'),
    path('products/',views.products, name='products'),
    path('products/pathpro/',views.path_pro, name='path_pro'),
    path('products/time-track/',views.time_track, name='time_track'),
    path('products/pathpro/quiz/',views.quiz_view, name='quiz_view'),
    path('products/habitpro/',views.habits_pro, name='habits_pro'),
    path('my-roadmaps/',views.my_roadmaps, name='my_roadmaps'),
    path('save_roadmap/', views.save_roadmap, name='save_roadmap'),
    path('priority/', views.priority, name='priority'),
    # path('get_user_priorities/', views.get_user_priorities, name='get_user_priorities'),
    # path('submit_priorities/', views.submit_priorities, name='submit_priorities'),
    # path('get_priorities_data/', views.get_priorities_data, name='get_priorities_data'),
]