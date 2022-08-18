from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=255)
    upload = models.ImageField(null=True)
class ClassesAndStudents(models.Model):
    student = models.ForeignKey(User,null=True, on_delete=models.DO_NOTHING)
    Class = models.ForeignKey(Class,null=True, on_delete=models.DO_NOTHING)
class Message(models.Model):
    student = models.ForeignKey(User,null=True, on_delete=models.DO_NOTHING)
    Class = models.ForeignKey(Class,null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=5000, blank=False)
    def __str__(self):
        if(len(self.text)<=100):
            return self.text
        return self.text[0:100]
class Comment(models.Model):
    message=models.ForeignKey(Message, null=True, on_delete=models.DO_NOTHING)
    text=models.TextField(max_length=500)
    student = models.ForeignKey(User,null=True, on_delete=models.DO_NOTHING)
    