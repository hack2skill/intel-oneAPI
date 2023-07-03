from django.shortcuts import render

def gamify(request):
    return render(request, 'gamify.html', {})