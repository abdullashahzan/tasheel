from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="User")
    
    def __str__(self):
        return self.user.username

class Road(models.Model):
    direction = models.IntegerField(default=0)
    camera = models.IntegerField(default=0)