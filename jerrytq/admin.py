from django.contrib import admin

from jerrytq import models

class ProjectCreditAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('credits', 'image_links', 'project_links',)

class ImageLinkAdmin(admin.ModelAdmin):
    pass

class ProjectLinkAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.ProjectCredit, ProjectCreditAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ImageLink, ImageLinkAdmin)
admin.site.register(models.ProjectLink, ProjectLinkAdmin)