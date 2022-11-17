"""
fortress URL Configuration
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jerrytq/', include('jerrytq.urls')),
    path('spin/', include('spin.urls'))
] 
