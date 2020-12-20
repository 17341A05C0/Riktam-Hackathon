from django.db import models


class User(models.Model):
    name=models.TextField(max_length=100)
    mail=models.EmailField(unique=True,max_length=200)
    password=models.TextField(max_length=1000)
    photo=models.ImageField(upload_to ='data/')
    is_admin=models.BooleanField(default=False)
    time=models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption=models.TextField(max_length=200)
    location=models.TextField(max_length=200)
    votes=models.IntegerField(default=0)
    image=models.ImageField(upload_to='Issues/')
    time=models.DateTimeField(auto_now_add=True)
    Choices= (
        (1,'Submitted to the newspaper'),
        (2,'resolved'),
        (3,'no action taken'),
        (4,'open')
    )
    status=models.IntegerField(max_length=100,choices=Choices,default=4)


class Vote(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    issue_id=models.ForeignKey(Issue,on_delete=models.CASCADE)


    class Meta:
        unique_together = (("user_id", "issue_id"),)

class Message(models.Model):
    message=models.TextField(max_length=200)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    issue_id=models.ForeignKey(Issue,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)

