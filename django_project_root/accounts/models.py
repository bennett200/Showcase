from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid

# Create your models here.


        
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, blank=True, unique=False)
    profile_img = models.ImageField(null=True, blank=True, upload_to='images/', default='images/default/default.jpg')
    
    @property 
    def imageURL(self):
        try:
            url = self.profile_img.url
        except:
            url = ''
        return url
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.email


    