from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    '''Crate Club table with title & user Column.
        user would be current login user when performing any action on video club
    '''
    title =models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #Have one issue with null.. no need of null=True but need to check
    
class Video(models.Model):
    '''
    Create Video table with title, url, youtube_id and club bind to video
    '''
    title =models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

