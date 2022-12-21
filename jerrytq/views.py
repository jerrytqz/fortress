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

    project = Project.objects.filter(slug=project_slug).first()

    if not project: 
        return JsonResponse({'error': "There are currently no projects with that name."}, status=404)
        
    return JsonResponse({'project': {
        'name': project.name,
        'credits': [credit.name for credit in project.credits.all()],
        'startDate': str(project.start_date),
        'imageLinks': [{'url': link.url, 'alt': link.name} for link in project.image_links.all()],
        'description': project.description,
        'projectLinks': {link.type: link.url for link in project.project_links.all()}
    }})
