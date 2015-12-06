from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
    # the email is the unique id
    email_addr = models.CharField(max_length=60)
    password = models.CharField(max_length=20)
    user_name = models.CharField(max_length=40)
    # ip_addr = models.CharField(max_length=40)
    # used for communication
    status = models.BooleanField(default=False)
    token = models.CharField(max_length=256)
    # the time the user being created.
    time = models.DateTimeField("Login time")

    def __str__(self):
        return self.email_addr

# This table is used to search
class ProjectInfo(models.Model):
    email_addr = models.CharField(max_length=60)
    user_name = models.CharField(max_length=40)
    project_name = models.CharField(max_length=50)
    project_status = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name

# one person can have many personal projects.
class PersonalProject(models.Model):
    personalinfo = models.ForeignKey(PersonalInfo)
    project_name = models.CharField(max_length=40)

    def __str__(self):
        return self.project_name

