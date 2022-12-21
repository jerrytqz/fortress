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
    WEBSITE = 'WEB'
    GITHUB = 'GIT'
    LINK_TYPE_CHOICES = [
        (WEBSITE, 'Website'),
        (GITHUB, 'GitHub')
    ]

    name = models.CharField(max_length=32)
    url = models.URLField()
    type = models.CharField(max_length=3, choices=LINK_TYPE_CHOICES, default=WEBSITE) 

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class Project(models.Model):
    name = models.CharField(unique=True, max_length=32)
    slug = models.SlugField(unique=True, null=False)
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
