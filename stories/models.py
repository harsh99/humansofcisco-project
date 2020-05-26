from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    title= models.CharField(max_length=100)
    fullstory= models.TextField()
    image= models.ImageField(upload_to='story/images/')
    created= models.DateTimeField(auto_now_add=True)
    viewcount= models.IntegerField(default=0)
    reactcount= models.IntegerField(default=0)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
