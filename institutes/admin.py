from django.contrib import admin

# Register your models here.
from institutes.models import Institute, StaffProfile, VisitedUsers

admin.site.register(Institute)
admin.site.register(StaffProfile)
admin.site.register(VisitedUsers)