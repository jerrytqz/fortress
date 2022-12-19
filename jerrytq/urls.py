from django.urls import path
from jerrytq import views

urlpatterns = [
    path('fetch-project-names', views.fetch_project_names, name='fetch_project_names')
]
