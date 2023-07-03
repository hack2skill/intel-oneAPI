from django.shortcuts import render, redirect
from login_register.models import Student, Rank, Attendance, Assignment, VirtualPet, ClassRank, SectionRank
import json

def dashboard(request):
    if 'student_id' in request.session:
        student_id = request.session['student_id']
        current_student = Student.objects.get(id=student_id)
        student_name = current_student.student_name

        # Get the current student's rank
        current_rank = Rank.objects.filter(student=current_student).first()

        # Get the ranks of other students around the current student's rank
        if current_rank:
            rank_difference = 5  # Number of ranks above and below the current rank to fetch
            rank_start = current_rank.rank - rank_difference if current_rank.rank else 1
            rank_end = current_rank.rank + rank_difference if current_rank.rank else rank_difference * 2
            other_ranks = Rank.objects.filter(rank__range=(rank_start, rank_end)).exclude(student=current_student)

            # Create the chart data for normal ranks
            normal_rank_data = {
                'labels': [],
                'datasets': [{
                    'label': 'Normal Rank',
                    'data': [],
                    'backgroundColor': '#C4B0FF',
                }]
            }

            for rank in other_ranks:
                normal_rank_data['labels'].append(rank.student.student_name)  # Add student name as label
                normal_rank_data['datasets'][0]['data'].append(rank.rank)  # Add rank as data
        else:
            other_ranks = None
            normal_rank_data = None

        # Get the average attendance of the current student
        average_attendance = Attendance.objects.filter(student=current_student).values('average_attendance')

        # Get the attendance of the current student in each subject
        attendance = Attendance.objects.get(student=current_student)

        # Get the completed number of assignments and total assignments of the current student
        assignments = Assignment.objects.get(student=current_student)
        assignments_remaining = assignments.total_assignments - assignments.completed_assignments

        # Get the pet details of the current student
        try:
            current_pet = VirtualPet.objects.get(student=current_student)
        except VirtualPet.DoesNotExist:
            current_pet = None

        # Get the current student's pet rank
        try:
            current_pet_rank = Rank.objects.get(student=current_student)
        except Rank.DoesNotExist:
            current_pet_rank = None

        # Get the ranks of other pets around the current student's pet rank
        if current_pet_rank:
            pet_rank_difference = 5  # Number of pet ranks above and below the current pet rank to fetch
            pet_rank_start = current_pet_rank.rank - pet_rank_difference
            pet_rank_end = current_pet_rank.rank + pet_rank_difference
            other_pet_ranks = Rank.objects.filter(rank__gte=pet_rank_start, rank__lte=pet_rank_end).exclude(student=current_student)
        else:
            other_pet_ranks = Rank.objects.all()

        # Get the pet details and pet names of other users' ranks
        other_pet_ranks_with_pet = []
        labels = []
        for rank in other_pet_ranks:
            try:
                pet = VirtualPet.objects.get(student=rank.student)
                other_pet_ranks_with_pet.append(pet)
                labels.append(pet.pet_name)
            except VirtualPet.DoesNotExist:
                continue

        # Create chart data for pet ranks
        pet_chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Pet Rank',
                    'data': [rank.rank for rank in other_pet_ranks],
                    'backgroundColor': '#C4B0FF',
                }
            ]
        }

        # Get section-wise ranks
        section_ranks = SectionRank.objects.filter(class_name=current_student.class_name, section=current_student.section)

        # Create section-wise rank data for chart
        section_wise_rank_data = {
            'labels': [],
            'datasets': []
        }

        for section_rank in section_ranks:
            section_name = section_rank.section
            ranks = section_rank.ranks.all()

            section_wise_rank_data['labels'].append(section_name)

            dataset = {
                'label': section_name,
                'data': [rank.rank for rank in ranks],
                'backgroundColor': '#C4B0FF'
            }
            section_wise_rank_data['datasets'].append(dataset)

        # Get class-wise ranks
        class_ranks = ClassRank.objects.filter(class_name=current_student.class_name)

        # Create class-wise rank data for chart
        class_wise_rank_data = {
            'labels': [],
            'datasets': [{
                'label': 'Class-wise Rank',
                'data': [],
                'backgroundColor': '#C4B0FF',
            }]
        }

        for class_rank in class_ranks:
            for rank in class_rank.ranks.all():
                class_wise_rank_data['labels'].append(rank.student.student_name)  # Add student name as label
                class_wise_rank_data['datasets'][0]['data'].append(rank.rank)  # Add rank as data

        chartData1 = json.dumps(class_wise_rank_data)
        chartData2 = json.dumps(section_wise_rank_data)
        chartData3 = json.dumps(normal_rank_data)
        chartData4 = json.dumps(pet_chart_data)

        context = {
            'student_name': student_name,
            'current_rank': current_rank,
            'other_ranks': other_ranks,
            'normal_rank_data': chartData3,
            'average_attendance': average_attendance,
            'attendance': attendance,
            'assignments': assignments,
            'assignments_remaining': assignments_remaining,
            'current_pet': current_pet,
            'current_pet_rank': current_pet_rank,
            'other_pet_ranks_with_pet': other_pet_ranks_with_pet,
            'pet_chart_data': chartData4,
            'section_wise_rank_data': chartData2,
            'class_wise_rank_data': chartData1,
        }

        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')

