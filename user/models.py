from django.db import models


class User(models.Model):
    name=models.TextField(max_length=100)
    mail=models.EmailField(unique=True,max_length=200)
    password=models.TextField(max_length=1000)
    photo=models.ImageField(upload_to ='data/')
    time=models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption=models.TextField(max_length=200)
    location=models.TextField(max_length=200)
    likes=models.IntegerField(default=0)
    image=models.ImageField(upload_to='posts/')
    time=models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)


class Comment(models.Model):
    comment=models.TextField(max_length=200)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)

