from django.shortcuts import render, redirect
from .models import Student, Marks, Attendance, Assignment, Pet
from django.core.exceptions import ValidationError
import random
import json

def logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        # Retrieve form data
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        class_name = request.POST.get('class')
        section = request.POST.get('section')
        favourite_categories = request.POST.getlist('favourite_categories')

        # Perform validation logic here
        if password != confirm_password:
            error_message = "Passwords do not match!!"
            return render(request, 'register.html', {'error_message': error_message})

        try:
            # Check if the email already exists in the database
            existing_student = Student.objects.get(email=email)
            error_message = "Email already exists!!"
            return render(request, 'register.html', {'error_message': error_message})
        except Student.DoesNotExist:
            pass

        # Save the registration details to the database
        student = Student(student_name=student_name, email=email, password=password, class_name=class_name, section=section, favourite_categories = favourite_categories)
        student.save()

        # Generate random marks
        maths_marks = random.randint(0, 100)
        hindi_marks = random.randint(0, 100)
        english_marks = random.randint(0, 100)
        science_marks = random.randint(0, 100)
        social_science_marks = random.randint(0, 100)

        # Save the marks to the database
        marks = Marks(
            student=student,
            maths=maths_marks,
            hindi=hindi_marks,
            english=english_marks,
            science=science_marks,
            social_science=social_science_marks
        )
        marks.save()

        # Generate random attendance percentages for each subject
        maths_attendance = random.randint(70, 100)
        hindi_attendance = random.randint(70, 100)
        english_attendance = random.randint(70, 100)
        science_attendance = random.randint(70, 100)
        social_science_attendance = random.randint(70, 100)

        # Save the attendance record
        attendance = Attendance(student=student, maths_attendance=maths_attendance, hindi_attendance=hindi_attendance,
                               english_attendance=english_attendance, science_attendance=science_attendance,
                               social_science_attendance=social_science_attendance)
        attendance.save()

        # Generate random completed assignments
        completed_assignments = random.randint(0, 6)

        # Create the Assignment object for the student
        assignment = Assignment(student=student, completed_assignments=completed_assignments, total_assignments=6)
        assignment.save()

        # Generate random values for pet level and pet progress
        pet_level = random.randint(1, 10)
        pet_progress = random.randint(0, 100)

        # Create the pet object associated with the student
        pet = Pet.objects.create(
            student=student,
            pet_name='\'NA\'',
            pet_type='',
            pet_level=pet_level,
            pet_progress=pet_progress,
            pet_coins=200
        )

        # Redirect to the dashboard page or any other page
        request.session['student_id'] = student.id  # Store the student ID in session
        return redirect('dashboard')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('Email_Id')
        password = request.POST.get('password')
        
        # Perform authentication/validation logic here
        try:
            student = Student.objects.get(email=email)
            if student.password == password:
                request.session['student_id'] = student.id  # Store the student ID in session
                return redirect('dashboard')  # Redirect to the dashboard page
            else:
                error_message = "Invalid email or password"
        except Student.DoesNotExist:
            error_message = "Invalid email or password"
            
        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
