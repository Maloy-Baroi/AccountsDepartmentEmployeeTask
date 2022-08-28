from django.contrib import admin
from App_auth.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(EmployeeProfileModel)
admin.site.register(BossModel)

