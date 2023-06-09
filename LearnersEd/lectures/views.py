from django.shortcuts import render

def lectures(request):
    return render(request, 'lectures.html', {})
