from django.shortcuts import render

def student_insights(request):
    return render(request, 'student_insights.html', {})
