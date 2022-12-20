from django.db import models

class ImageLink(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class ProjectCredit(models.Model):
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class ProjectLink(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField()  

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class Project(models.Model):
    name = models.CharField(unique=True, max_length=32)
    slug = models.SlugField(null=False, default="")
    credits = models.ManyToManyField(ProjectCredit)
    start_date = models.DateField()
    image_links = models.ManyToManyField(ImageLink)
    description = models.TextField(default="")
    project_links = models.ManyToManyField(ProjectLink)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['order']
