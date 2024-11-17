from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomerUser(AbstractUser):
    user_picture = models.ImageField(default='https://cdn-icons-png.flaticon.com/512/3334/3334385.png',upload_to='media/')




class Friendship(models.Model):
    sender = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='friendship_sender')
    receiver = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='friendship_receiver')
    status = models.CharField(max_length=10, default='pending')