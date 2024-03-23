
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 
urlpatterns = [
    path('joincall/',views.joincall,name='videocall'),
    path('mentorlist/',views.listrooms,name='videocall'),
    path('createmeet/',views.createmeet,name='createmeet'),
]
