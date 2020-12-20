from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('user.urls')),
    path('superadmin/', admin.site.urls),
]
