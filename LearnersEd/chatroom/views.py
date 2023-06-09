from django.shortcuts import render
from django.http import JsonResponse
from login_register.models import Student
from .models import ChatMessage
from datetime import datetime

def chatroom(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')  # Retrieve student ID from the session
        message = request.POST['message']
        student = Student.objects.get(id=student_id)
        ChatMessage.objects.create(student=student, message=message)
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         # Get the student's name
        student_id = request.session.get('student_id')
        student = Student.objects.get(id=student_id)
        student_name = student.student_name

        # Construct the response
        response = {
            'student': student_name,
            'message': message,
            'timestamp': timestamp
        }

        return JsonResponse(response)

    students = Student.objects.all()
    messages = ChatMessage.objects.all()
    return render(request, 'chatroom.html', {'students': students, 'messages': messages})

