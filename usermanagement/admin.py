from django.contrib import admin

from usermanagement.models import CustomerProfile, UserFeedback, UserPositivityLog

admin.site.register(CustomerProfile)
admin.site.register(UserFeedback)
admin.site.register(UserPositivityLog)