from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline

from jerrytq import models


class ImageLinkAdmin(admin.ModelAdmin):
    pass


class ProjectLinkAdmin(admin.ModelAdmin):
    pass


class TechnologyAdmin(admin.ModelAdmin):
    pass


class SkillAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


class ProjectCreditToProjectInline(SortableTabularInline, admin.TabularInline):
    model = models.Project.project_credits.through
    verbose_name = 'project credit'
    extra = 0


class ImageLinkToProjectInline(SortableTabularInline, admin.TabularInline):
    model = models.Project.image_links.through
    verbose_name = 'image link'
    extra = 0
    min_num = 1


class TechnologyToProjectInline(SortableTabularInline, admin.TabularInline):
    model = models.Project.technologies.through
    verbose_name = 'technology'
    verbose_name_plural = 'technologies'
    extra = 0


class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    # filter_horizontal = ('project_links',)
    inlines = (ProjectCreditToProjectInline, ImageLinkToProjectInline, TechnologyToProjectInline)


class TermAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


class ExperienceAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(models.ImageLink, ImageLinkAdmin)
admin.site.register(models.ProjectLink, ProjectLinkAdmin)
admin.site.register(models.Technology, TechnologyAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Experience, ExperienceAdmin)
