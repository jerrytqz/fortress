from jerrytq.forms import ContactForm
from jerrytq.models import Project, Course, Technology, Skill, Experience
import os
import importlib

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User as AdminUser
from django.template.loader import render_to_string
from django.utils import timezone
settings = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])


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
        return JsonResponse({'error': "There are no projects with that name."}, status=404)

    return JsonResponse({'project': {
        'name': project.name,
        'projectCredits': [
            cred.name for cred in project.project_credits.all().order_by('projectcredittoproject')
        ],
        'startDate': str(project.start_date),
        'imageLinks': [{
            'url': link.url,
            'alt': link.name
        } for link in project.image_links.all().order_by('imagelinktoproject')],
        'description': project.description,
        'projectLinks': {link.type: link.url for link in project.project_links.all()},
        'technologies': [{
            'name': tech.name,
            'imageLink': {
                'url': tech.image_link.url,
                'alt': tech.image_link.name
            }
        } for tech in project.technologies.all().order_by('technologytoproject')]
    }})


def fetch_skills(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    return JsonResponse({'skills': {
        'languages': [{
            'name': skill.technology.name,
            'proficiency': skill.get_proficiency_display(),
            'imageLink': {
                'url': skill.technology.image_link.url,
                'alt': skill.technology.image_link.name
            }
        } for skill in Skill.objects.filter(technology__type=Technology.LANGUAGE)],
        'frameworks': [{
            'name': skill.technology.name,
            'proficiency': skill.get_proficiency_display(),
            'imageLink': {
                'url': skill.technology.image_link.url,
                'alt': skill.technology.image_link.name
            }
        } for skill in Skill.objects.filter(technology__type=Technology.FRAMEWORK)],
        'libraries': [{
            'name': skill.technology.name,
            'proficiency': skill.get_proficiency_display(),
            'imageLink': {
                'url': skill.technology.image_link.url,
                'alt': skill.technology.image_link.name
            }
        } for skill in Skill.objects.filter(technology__type=Technology.LIBRARY)],
        'tools': [{
            'name': skill.technology.name,
            'proficiency': skill.get_proficiency_display(),
            'imageLink': {
                'url': skill.technology.image_link.url,
                'alt': skill.technology.image_link.name
            }
        } for skill in Skill.objects.filter(technology__type=Technology.TOOL)],
        'platforms': [{
            'name': skill.technology.name,
            'proficiency': skill.get_proficiency_display(),
            'imageLink': {
                'url': skill.technology.image_link.url,
                'alt': skill.technology.image_link.name
            }
        } for skill in Skill.objects.filter(technology__type=Technology.PLATFORM)]
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
        'description': course.description
    } for course in courses]})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_email = form.cleaned_data['sender_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject=subject,
                message=message,
                html_message=render_to_string('contact_email.html', {
                    'sender_name': sender_name,
                    'sender_email': sender_email,
                    'message': message,
                    'date_time': timezone.now()
                }),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=AdminUser.objects.filter(is_superuser=True).values_list(
                    'email',
                    flat=True
                ),
                fail_silently=False
            )
            return JsonResponse({})
        else:
            return JsonResponse({'form': form.as_div()}, status=400)
    else:
        form = ContactForm()
        return JsonResponse({'form': form.as_div()})


def fetch_experiences(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    experiences = Experience.objects.all()

    return JsonResponse({'experiences': [{
        'title': experience.title,
        'company': experience.company,
        'location': experience.location,
        'startDate': str(experience.start_date.strftime("%b %Y")),
        'endDate': str(experience.end_date.strftime("%b %Y")),
        'imageLink': {
            'url': experience.image_link.url,
            'alt': experience.image_link.name
        }
    } for experience in experiences]})


def fetch_project_cards(request):
    if request.method != 'GET':
        return JsonResponse({'error': "Request error"}, status=400)

    projects = Project.objects.all()

    return JsonResponse({'projectCards': [{
        'name': project.name,
        'slug': project.slug,
        'imageLink': {
            'url': project.image_links.all().first().url if project.image_links.exists() else '',
            'alt': project.image_links.all().first().name if project.image_links.exists() else ''
        },
        'shortDescription': project.short_description
    } for project in projects]})
