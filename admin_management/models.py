from django.db import models

# Create your models here.

class StudentData(models.Model):
    school = models.CharField(max_length=240, null=True, blank=True)
    standard = models.IntegerField(max_length=240, null=True, blank=True)
    subject = models.CharField(max_length=30, null=True, blank=True)
    student = models.CharField(max_length=240, null=True, blank=True)
    term = models.IntegerField(max_length=240, null=True, blank=True)
    mark = models.IntegerField(max_length=240, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, max_length=240, null=True, blank=True)
