from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images', null=True, blank=True)
    mobile = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name

class Institute(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True)
    staff = models.OneToOneField(StaffProfile, related_name="my_instituite", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VisitedUsers(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    instituite = models.ForeignKey(Institute, on_delete=models.CASCADE)
    visited_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)