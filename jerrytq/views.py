from django.shortcuts import render
from django.http import JsonResponse

from jerrytq import models

def fetch_projects(request):
    response = []

    for project in models.Project.objects.all():
        response.append(project.name)

    return JsonResponse({'projects': response})
