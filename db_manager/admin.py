from django.contrib import admin

# Register your models here.
from .models import PersonalInfo, ProjectInfo, PersonalProject

class PersonalInfoAdmin(admin.ModelAdmin):
    fields = ['user_name', 'email_addr', 'password', 'status', 'token', 'time']

class ProjectInfoAdmin(admin.ModelAdmin):
    fields = ['project_name', 'project_status', 'email_addr', 'user_name']

admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(ProjectInfo, ProjectInfoAdmin)
admin.site.register(PersonalProject)
