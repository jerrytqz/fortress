from django.urls import path
from jerrytq import views

urlpatterns = [
    path('fetch-projects', views.fetch_projects, name='fetch_projects')
]
