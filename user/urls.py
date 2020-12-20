from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name="user"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('addvote/',views.addvote,name='addvote'),
    path('addmessage/',views.addmessage,name='addmessage'),
    path('profile/',views.profile,name="profile"),
    path('editTitle',views.editTitle,name="editTitle"),
    path('deleteIssue',views.deleteIssue,name="deleteIssue"),
    path('deleteMessage',views.deleteMessage,name="deleteMessage"),
    path('admin',views.admin,name="admin"),
    path('logout',views.logout,name="logout")
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



