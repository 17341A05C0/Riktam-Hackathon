from django.db import models


class User(models.Model):
    name=models.TextField(max_length=100)
    mail=models.EmailField(unique=True,max_length=200)
    password=models.TextField(max_length=20)
    photo=models.ImageField(upload_to ='data/')
    time=models.DateTimeField(auto_now_add=True)