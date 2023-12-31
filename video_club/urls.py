"""
URL configuration for video_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path
from club import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    #AUTH Urls
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    #Club Urls
    path('clubofframe/create', views.CreateClub.as_view(), name='create_club'),
    path('clubofframe/<int:pk>', views.DetailClub.as_view(), name='detail_club'),
    path('clubofframe/<int:pk>/update', views.UpdateClub.as_view(), name='update_club'),
    path('clubofframe/<int:pk>/delete', views.DeleteClub.as_view(), name='delete_club'),

    #Video Urls
   path('clubofframe/<int:pk>/addvideo', views.add_video, name='add_video'),
   path('video/search', views.video_search, name='video_search'),
   path('clubofframe/<int:pk>/deletevideo', views.DeleteVideo.as_view(), name='delete_video'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)