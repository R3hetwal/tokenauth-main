from django.db import models
from users.models import User, Address
from ckeditor.fields import RichTextField
import uuid
from datetime import date, datetime
from django.db.models import QuerySet as Q
from django.contrib.gis.db import models


# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    project_members = models.ManyToManyField(User, related_name='people_involved')
    description = models.TextField(null = True, blank = True)
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    
    @property
    def days_since_start(self):
        if self.start_date is not None:
            today = date.today()
            days_since_start = (today - self.start_date).days
            return days_since_start
        return None
        
    @property
    def days_remaining(self):
        if self.days_remaining is not None:
            today = date.today()
            days_remaining = (self.start_date - days_remaining).days
            return days_remaining
        return None
    
    def __str__(self):
        return self.project_name
    
class Department(models.Model):
    department_name = models.CharField(max_length=255)
    department_head = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_head', null=True)
    members = models.ManyToManyField(User)                                                                                                                                                                
    creation_date = models.DateField(blank=True, null=True)
    project = models.ManyToManyField(Project)
   
    @property
    def active_days(self):
        if self.creation_date is not None:
            today = date.today()
            active_days = (today - self.creation_date).days
            return active_days
        return None

    def __str__(self):
        return self.department_name
 
class Document(models.Model):
    document_name = models.CharField(max_length=255, default='Document')
    document_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='document_owner')
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_name_for_document')
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='department_name_for_document')
    created_at = models.DateTimeField(blank=True, null=True)
    identifier = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    # additional_docs = models.ManyToManyField('AdditionalDoc', blank=True)
    
    def __str__(self):
        return self.document_name


class AdditionalDoc(models.Model):
    additional_documents = models.ForeignKey(Document, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to="additional_docs/")


class ProjectSite(models.Model):
    site_name=models.CharField(max_length=255)
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_site', null=True, blank=True)
    site_location=models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)
    site_area=models.PolygonField(blank=True, null=True)
    way=models.LineStringField(blank=True, null=True)

    def __str__(self):
        return self.site_name