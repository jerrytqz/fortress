from django.shortcuts import render
from django.http import JsonResponse

from jerrytq.models import Project, Course

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
        'projectCredits': [credit.name for credit in project.project_credits.all().order_by('projectcredittoproject')],
        'startDate': str(project.start_date),
        'imageLinks': [{'url': link.url, 'alt': link.name} for link in project.image_links.all().order_by('imagelinktoproject')],
        'description': project.description,
        'projectLinks': {link.type: link.url for link in project.project_links.all()},
        'technologies': [{'name': tech.name, 'imageLink': {'url': tech.image_link.url, 'alt': tech.image_link.name}} for tech in project.technologies.all().order_by('technologytoproject')]
    }})

def fetch_courses(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    term_name = request.GET.get('termName', '')

    courses = Course.objects.filter(term__name=term_name)

    if not courses:
        return JsonResponse({'error': "No courses were found for that term."}, status=404)

    return JsonResponse({'courses': [{
        'term': {'name': course.term.name, 'period': course.term.period},
        'name': course.name,
        'description': course.description,
        'grade': course.grade
    } for course in courses]})
