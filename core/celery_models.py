from django.db import models

class SummaryData(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    total_projects = models.IntegerField(null=True, blank=True)
    total_users = models.IntegerField(null=True, blank=True)