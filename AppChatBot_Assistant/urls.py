from django.urls import path
from . import views
from AppChatBot_Assistant.views import Message

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('Logout/', views.Logout, name='Logout'),
    path('Login/',views.Login,name='Login'),
    path('Registeration/',views.Registeration,name='Registeration'),
    path('EditDetails/', views.EditDetails, name='EditDetails'),
    path('Message/', Message.as_view(),name='Message'),
    path('ChatWindow/', views.ChatWindow, name='ChatWindow'),
    path('ChatWindows/', views.ChatWindows, name='ChatWindows'),



]
