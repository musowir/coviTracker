from django.contrib import admin

# Register your models here.
from institutes.models import Institute, StaffProfile, VisitedUsers, AlertLog

admin.site.register(Institute)
admin.site.register(StaffProfile)
admin.site.register(VisitedUsers)
admin.site.register(AlertLog)