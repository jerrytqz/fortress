from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from jerrytq import models

class ImageLinkAdmin(admin.ModelAdmin):
    pass

class ProjectCreditAdmin(admin.ModelAdmin):
    pass

class ProjectLinkAdmin(admin.ModelAdmin):
    pass

class TechnologyAdmin(admin.ModelAdmin):
    pass

class SkillAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ('credits', 'image_links', 'project_links', 'technologies')

admin.site.register(models.ImageLink, ImageLinkAdmin)
admin.site.register(models.ProjectCredit, ProjectCreditAdmin)
admin.site.register(models.ProjectLink, ProjectLinkAdmin)
admin.site.register(models.Technology, TechnologyAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Project, ProjectAdmin)
