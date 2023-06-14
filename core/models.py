from django.db import models
# from users.models import User, Address
from ckeditor.fields import RichTextField
import uuid
from datetime import date, datetime
from django.db.models import QuerySet as Q
from django.contrib.gis.db import models
from django.contrib.gis.db import models as gismd

# Create your models here.
class ProjectStatus(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    status = models.BooleanField(default=True, blank=True)
    project = models.ForeignKey("Project", related_name="status_project",
                                on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def delete(self):
        self.status = False
        self.save()

    def __str__(self):
        return f"{self.name} ({self.pk})"

class Project(models.Model):
    # owner = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.OneToOneField('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='projects_owned')
    project_name = models.CharField(max_length=255)
    # project_members = models.ManyToManyField(User, related_name='people_involved')
    projectstatus = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
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
        return f"{self.project_name} ({self.pk})"

class Department(models.Model):
    from users.models import User

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
    from users.models import User

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

# class Path(models.Model):
#     home = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='home')
#     site_address = models.CharField(null=True, blank=True)
#     # site_loc = models.PointField(null=True, blank=True, srid=4326)

#     def __str__(self):
#         return self.site_address


class ProjectSiteAddress(models.Model):
    geom = gismd.GeometryField(srid=4326)
    geom_type = models.CharField(max_length=20, blank=True, null=True)
    area = models.FloatField(null=True, blank=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="projectsites"
    )


'''For Dummy Data Creation'''
class ProjectSite(models.Model):
    site_loc=models.PointField(blank=True, null=True)
    site_area=models.PolygonField(blank=True, null=True)
