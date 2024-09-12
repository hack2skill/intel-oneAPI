from django.contrib import admin
from django.urls import path
from chatbot.views import chatbot
from virtual_pet.views import virtual_pet
from Gamify_Quiz.views import gamify_quiz
from dashboard.views import dashboard
from lectures.views import lectures
from explore_fields.views import explore_fields
from login_register.views import login, register, logout
from gamify_app.views import gamify
from student_insights_app.views import student_insights
from chatroom.views import chatroom
from lecture_attend.views import lecture_attend
from assignment.views import assignment
from .views import *;

urlpatterns = [
    path("", register),
    path("login/", login),
    path("register/", register),
    path('admin/', admin.site.urls),
    path('chatbot/', chatbot),
    path('virtual-pet/', virtual_pet),
    path('gamify-quiz/', gamify_quiz),
    path('dashboard/', dashboard, name='dashboard'),
    path('explore-fields/', explore_fields),
    path('lectures/', lectures),
    path('gamify/', gamify),
    path('student_insights/', student_insights),
    path('logout/', logout),
    path('lecture_attend/', lecture_attend),
    path('chatroom/', chatroom),
    path('assignment/', assignment)
]
