from django.shortcuts import render
from login_register.models import VirtualPet
from django.http import JsonResponse    

def virtual_pet(request):
    # if 'student_id' in request.session:
    #     if request.method == 'POST':
    #         if request.POST.get('level'):
    #             level = request.POST.get('level')
    #             progress = request.POST.get('progress')
    #             coin = request.POST.get('coin')
    #             pet = VirtualPet.objects.get(id=student_id)  # Assuming there's only one pet record
    #             pet.pet_level = level
    #             pet.pet_level_progress = progress
    #             pet.pet_coin = coin
    #             pet.save()
    #             return JsonResponse({'status': 'success'})
    #     student_id = request.session['student_id']
    #     pet = VirtualPet.objects.get(id=student_id)
    #     pet_data = {
    #         'name': pet.pet_name,
    #         'type': pet.pet_type,
    #         'level': pet.pet_level,
    #         'progress': pet.pet_level_progress,
    #         'pet_coin': pet.pet_coin
    #     }
    #     return JsonResponse({'pet': pet_data})
    return render(request, "virtual-pet.html", {})
