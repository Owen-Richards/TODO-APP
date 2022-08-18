from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class PDF(models.Model):
    description=models.TextField(max_length=500, null=False, blank=False)
    PDF=models.FileField(null=False)
    category=models.ForeignKey('classes.Class', on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User,null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description

# Create your models here.
