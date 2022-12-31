from django.db import models
from django.core.validators import MaxValueValidator

class ImageLink(models.Model):
    name = models.CharField(unique=True, max_length=64)
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

    name = models.CharField(unique=True, max_length=32)
    url = models.URLField()
    type = models.CharField(max_length=3, choices=LINK_TYPE_CHOICES, default=WEBSITE) 

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class Technology(models.Model):
    LANGUAGE = 'LAN'
    FRAMEWORK = 'FRA'
    LIBRARY = 'LIB'
    TOOL = 'TOO'
    PLATFORM = 'PLA'
    TECH_TYPE_CHOICES = [
        (LANGUAGE, 'Language'),
        (FRAMEWORK, 'Framework'),
        (LIBRARY, 'Library'),
        (TOOL, 'Tool'),
        (PLATFORM, 'Platform')
    ]

    name = models.CharField(unique=True, max_length=32)
    image_link = models.ForeignKey(ImageLink, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=3, choices=TECH_TYPE_CHOICES, default=LANGUAGE)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name_plural = 'technologies'
        ordering = ['name']

class Skill(models.Model):
    BASIC = 'BAS'
    INTERMEDIATE = 'INT'
    ADVANCED = 'ADV'
    PROFICIENCY_CHOICES = [
        (BASIC, 'Basic'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced')
    ]

    technology = models.OneToOneField(Technology, on_delete=models.CASCADE, null=True)
    proficiency = models.CharField(max_length=3, choices=PROFICIENCY_CHOICES, default=BASIC)

    def __str__(self):
        return self.technology.name

    class Meta: 
        ordering = ['technology__name']

class Project(models.Model):
    name = models.CharField(unique=True, max_length=32)
    slug = models.SlugField(unique=True, null=False)
    project_credits = models.ManyToManyField(
        ProjectCredit, 
        through='ProjectCreditToProject'
    )
    start_date = models.DateField()
    image_links = models.ManyToManyField(
        ImageLink,
        through='ImageLinkToProject'
    )
    description = models.TextField(default="")
    project_links = models.ManyToManyField(ProjectLink)
    technologies = models.ManyToManyField(
        Technology,
        through='TechnologyToProject'
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    
    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['order']

class TechnologyToProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.project.name}: {self.technology.name}"

    class Meta: 
        ordering = ['order']

class ImageLinkToProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image_link = models.ForeignKey(ImageLink, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.project.name}: {self.image_link.name}"

    class Meta: 
        ordering = ['order']

class ProjectCreditToProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_credit = models.ForeignKey(ProjectCredit, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.project.name}: {self.project_credit.name}"

    class Meta: 
        ordering = ['order']

class Term(models.Model):
    name = models.CharField(unique=True, max_length=4)
    period = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.period})"

class Course(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=64)
    grade = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        MaxValueValidator(100)
    ])
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"({self.term.name}) {self.name} {self.description}"

    class Meta: 
        ordering = ['order']
