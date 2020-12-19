from django.contrib import admin

# Register your models here.
from .models import User, Issue, Vote, Message
admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Vote)
admin.site.register(Message)