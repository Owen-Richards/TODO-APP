from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #try taking this out
    name = models.CharField(max_length=50, null=True, blank=True)
    #userEvents = ArrayField(Event) #1

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    author = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING) #2
    start_time_string=models.TextField(null=True)
    end_time_string=models.TextField(null=True)
    @property
    def get_html_url(self):
        url = reverse('oauth_app:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'