from django.shortcuts import render, redirect
from login_register.models import Student, Attendance, Assignment, Pet
import json

def dashboard(request):
    if 'student_id' in request.session:
        student_id = request.session['student_id']
        current_student = Student.objects.get(id=student_id)
        student_name = current_student.student_name

        # Get the current student's rank, class rank, and section rank
        current_rank = current_student.rank
        current_class_rank = current_student.class_rank
        current_section_rank = current_student.section_rank
        current_pet_rank = current_student.pet_rank

        # Initialize the rank ranges for fetching students
        rank_start = current_rank - 2
        rank_end = current_rank + 2

        class_rank_start = current_class_rank - 2
        class_rank_end = current_class_rank + 2

        section_rank_start = current_section_rank - 2
        section_rank_end = current_section_rank + 2

        pet_rank_start = current_pet_rank - 2
        pet_rank_end = current_pet_rank + 2

        # Adjust rank ranges based on current student's rank, class rank, and section rank
        if current_rank == 1:
            rank_start = 1
            rank_end = current_rank + 4
        elif current_rank == 2:
            rank_start = 1
            rank_end = current_rank + 3
        elif current_rank == Student.objects.count():
            rank_start = current_rank - 4
            rank_end = current_rank
        elif current_rank == Student.objects.count() - 1:
            rank_start = current_rank - 3
            rank_end = current_rank + 1

        if current_class_rank == 1:
            class_rank_start = 1
            class_rank_end = current_class_rank + 4
        elif current_class_rank == 2:
            class_rank_start = 1
            class_rank_end = current_class_rank + 3
        elif current_class_rank == Student.objects.filter(class_name=current_student.class_name).count():
            class_rank_start = current_class_rank - 4
            class_rank_end = current_class_rank
        elif current_class_rank == Student.objects.filter(class_name=current_student.class_name).count() - 1:
            class_rank_start = current_class_rank - 3
            class_rank_end = current_class_rank + 1

        if current_section_rank == 1:
            section_rank_start = 1
            section_rank_end = current_section_rank + 4
        elif current_section_rank == 2:
            section_rank_start = 1
            section_rank_end = current_section_rank + 3
        elif current_section_rank == Student.objects.filter(class_name=current_student.class_name, section=current_student.section).count():
            section_rank_start = current_section_rank - 4
            section_rank_end = current_section_rank
        elif current_section_rank == Student.objects.filter(class_name=current_student.class_name, section=current_student.section).count() - 1:
            section_rank_start = current_section_rank - 3
            section_rank_end = current_section_rank + 1

        if current_pet_rank == 1:
            pet_rank_start = 1
            pet_rank_end = current_pet_rank + 4
        elif current_pet_rank == 2:
            pet_rank_start = 1
            pet_rank_end = current_pet_rank + 3
        elif current_pet_rank == Student.objects.count():
            pet_rank_start = current_pet_rank - 4
            pet_rank_end = current_pet_rank
        elif current_pet_rank == Student.objects.count() - 1:
            pet_rank_start = current_pet_rank - 3
            pet_rank_end = current_pet_rank + 1

       # Get the students with ranks around the current student
        rank_students = Student.objects.filter(rank__range=(rank_start, rank_end)).order_by('-rank')

        # Get the students with class ranks around the current student
        class_rank_students = Student.objects.filter(class_name=current_student.class_name,
                                                    class_rank__range=(class_rank_start, class_rank_end)).order_by('-class_rank')

        # Get the students with section ranks around the current student
        section_rank_students = Student.objects.filter(class_name=current_student.class_name,
                                                    section=current_student.section,
                                                    section_rank__range=(section_rank_start, section_rank_end)).order_by('-section_rank')
        
        # Get the students with ranks around the current student
        pet_rank_students = Student.objects.filter(pet_rank__range=(pet_rank_start, pet_rank_end)).order_by('-pet_rank')

        # Prepare chart data for rank students
        rank_student_names = [student.student_name.split()[0] for student in rank_students]
        rank_student_data = [student.rank for student in rank_students]

        rank_chart_data = {
            'labels': rank_student_names,
            'datasets': [{
                'data': list(reversed(rank_student_data)),
                'backgroundColor': '#C4B0FF',
            }],
        }
        rank_chart_data = json.dumps(rank_chart_data)

        # Prepare chart data for class rank students
        class_rank_student_names = [student.student_name.split()[0] for student in class_rank_students]
        class_rank_student_data = [student.class_rank for student in class_rank_students]
        class_rank_chart_data = {
            'labels': class_rank_student_names,
            'datasets': [{
                'data': list(reversed(class_rank_student_data)),
                'backgroundColor': '#C4B0FF'
            }],
        }
        class_rank_chart_data = json.dumps(class_rank_chart_data)

        # Prepare chart data for section rank students
        section_rank_student_names = [student.student_name.split()[0] for student in section_rank_students]
        section_rank_student_data = [student.section_rank for student in section_rank_students]
        section_rank_chart_data = {
            'labels': section_rank_student_names,
            'datasets': [{
                'data': list(reversed(section_rank_student_data)),
                'backgroundColor': '#C4B0FF'
            }],
        }
        section_rank_chart_data = json.dumps(section_rank_chart_data)

        pet_rank_student_names = []
        for student in pet_rank_students:
            petName = Pet.objects.get(student = student).pet_name
            if (petName == '\'NA\''):
                pet_rank_student_names.append('NA')
            else:
                pet_rank_student_names.append(petName)

        pet_rank_student_data = [student.pet_rank for student in pet_rank_students]

        pet_rank_chart_data = {
            'labels': pet_rank_student_names,
            'datasets': [{
                'data': list(reversed(pet_rank_student_data)),
                'backgroundColor': '#C4B0FF',
            }],
        }
        pet_rank_chart_data = json.dumps(pet_rank_chart_data)

        # Access the favorite categories of the student
        favorite_categories = current_student.favourite_categories
        favorite_categories = json.dumps(favorite_categories)

        # Get the average attendance of the current student
        average_attendance = Attendance.objects.filter(student=current_student).values('average_attendance')

        # Get the attendance of the current student in each subject
        attendance = Attendance.objects.get(student=current_student)

        # Get the completed number of assignments and total assignments of the current student
        assignments = Assignment.objects.get(student=current_student)
        assignments_remaining = assignments.total_assignments - assignments.completed_assignments

        # Get the pet details of the current student
        current_pet = Pet.objects.get(student=current_student)

        context = {
            'student_name': student_name,
            'current_student': current_student,
            'current_rank': current_rank,
            'favorite_categories': favorite_categories,
            'average_attendance': average_attendance,
            'attendance': attendance,
            'assignments': assignments,
            'assignments_remaining': assignments_remaining,
            'current_pet': current_pet,
            'rank_chart_data': rank_chart_data,
            'class_rank_chart_data': class_rank_chart_data,
            'section_rank_chart_data': section_rank_chart_data,
            'pet_rank_chart_data': pet_rank_chart_data
        }

        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')