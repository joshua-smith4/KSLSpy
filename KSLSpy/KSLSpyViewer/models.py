from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queryJSON = models.CharField(max_length=10000, default='')
    notify = models.BooleanField(default=True)

class Result(models.Model):
    query = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    listingURL = models.CharField(max_length=500, default='', null=False)
    imageURL = models.CharField(max_length=500, default='')
    resultJSON = models.CharField(max_length=10000, default='', null=False)
    resultHash = models.BigIntegerField(default=0, null=False)