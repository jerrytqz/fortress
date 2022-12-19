from django.shortcuts import render
from django.http import JsonResponse

from jerrytq import models

def fetch_project_names(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    response = []

    for project in models.Project.objects.all():
        response.append({'name': project.name, 'urlName': project.url_name})

    return JsonResponse({'projectNames': response})
