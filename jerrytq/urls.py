from django.urls import path
from jerrytq import views

urlpatterns = [
    path('project-names/', views.project_names, name='project_names'),
    path('project/', views.project, name='project'),
    path('skills/', views.skills, name='skills'),
    path('courses/', views.courses, name='courses'),
    path('contact/', views.contact, name='contact'),
    path('experiences/', views.experiences, name='experiences'),
    path('project-cards/', views.project_cards, name='project_cards')
]
