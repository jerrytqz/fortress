from django.shortcuts import render
from django.http import JsonResponse

from jerrytq.models import Project

def fetch_project_names(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    response = []

    for project in Project.objects.all():
        response.append({'name': project.name, 'slug': project.slug})

    return JsonResponse({'projectNames': response})

def fetch_project(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)
    
    project_slug = request.GET.get('slug', '')

    if not Project.objects.filter(slug=project_slug).exists():
        return JsonResponse({'error': "There are currently no projects with that name."}, status=404)
    
    return JsonResponse({'hello': 'world'})
