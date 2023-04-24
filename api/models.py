from django.db import models
from users.models import User
from ckeditor.fields import RichTextField
import uuid
from datetime import date, datetime
from django.db.models import QuerySet as Q

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    start_date = models.DateField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    
    @property
    def days_since_start(self):
        if self.start_date is not None:
            today = date.today()
            days_since_start = (today - self.start_date).days
            return days_since_start
        return None
    
    def __str__(self):
        return self.project_name
    

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    department_head = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_head', null=True)
    members = models.ManyToManyField(User)                                                                                                                                                                
    creation_date = models.DateField(null=True, blank=True)
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
    document_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    # additional_docs = models.ManyToManyField('AdditionalDoc', blank=True)

    
    def __str__(self):
        return self.document_name


class AdditionalDoc(models.Model):
        additional_documents = models.ForeignKey(Document, on_delete=models.CASCADE, default=None)
        file = models.FileField(upload_to="additional_docs/")


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departments = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_involved')
    projects = models.ManyToManyField(Project)
    
    def __str__(self):
        return self.user.email

    def get_user_info(email):
        try:
            user = User.objects.get(email=email)
            user_info = UserInfo.objects.get(user=user)
            departments = user_info.departments.filter(members=user)
            projects = user_info.projects.all()
            documents = Document.objects.filter(project_name__in=projects)
            additional_docs = AdditionalDoc.objects.filter(additional_documents__in=documents)

            return {
                'user_info': user_info,
                'departments': departments,
                'projects': projects,
                'documents': documents,
                'additional_docs': additional_docs,
            }
        except (User.DoesNotExist, UserInfo.DoesNotExist):
            return None
