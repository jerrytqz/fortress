from django.urls import path
from jerrytq import views

urlpatterns = [
    path('fetch-project-names/', views.fetch_project_names, name='fetch_project_names'),
    path('fetch-project/', views.fetch_project, name='fetch_project'),
    path('fetch-skills/', views.fetch_skills, name='fetch_skills'),
    path('fetch-courses/', views.fetch_courses, name='fetch_courses'),
    path('contact/', views.contact, name='contact'),
    path('fetch-experiences/', views.fetch_experiences, name='fetch_experiences'),
    path('fetch-project-cards/', views.fetch_project_cards, name='fetch_project_cards')
]
