"""
fortress URL Configuration
"""

from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Fortress'
admin.site.site_title = 'Fortress'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jerrytq/', include('jerrytq.urls')),
    path('spin/', include('spin.urls'))
] 
