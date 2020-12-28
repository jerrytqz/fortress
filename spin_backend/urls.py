"""spin_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from leads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('purchase-spin/', views.purchase_spin, name='purchase_spin'),
    path('fetch-sp/', views.fetch_sp, name='set_sp'),
    path('auto-log-in/', views.auto_log_in, name='auto_log_in'),
    path('fetch-inventory/', views.fetch_inventory, name='fetch_inventory'),
    path('fetch-profile/', views.fetch_profile, name='fetch_profile'),
    path('free-sp/', views.free_sp, name='free_sp'),
    path('list-item/', views.list_item, name='list-item')
]
