from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.user_login,name='login_user'),
    path("signup/",views.signup,name='signup'),
    path('logout/', views.logout_user, name='logout_user'),
    path('products/',views.products, name='products'),
    path('products/pathpro/',views.path_pro, name='path_pro'),
    path('products/time-track/',views.time_track, name='time_track'),
    
]