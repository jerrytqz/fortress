from django.shortcuts import render
from django.http import JsonResponse

from jerrytq.models import Project

def fetch_project_names(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    response = []

    for project in Project.objects.all():
        response.append({'name': project.name, 'urlName': project.url_name})

    return JsonResponse({'projectNames': response})

def fetch_project(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)
    
    project_url_name = request.GET.get('urlName', '')

    if not Project.objects.filter(url_name=project_url_name).exists():
        return JsonResponse({'error': "There are currently no projects with that name."}, status=404);
    
    return JsonResponse({'hello': 'world'});
