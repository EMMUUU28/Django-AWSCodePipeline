from django.contrib import admin
from django.urls import path, include
# from .views import talkpdf, talkpdf1, category,ar
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path("resume/", views.talkpdf, name="talkpdf"),
    path('roadmap/',views.roadmap,name='roadmap'),
    path('test/',views.roadmap1,name='roadmap1'),
    # path('chat', views.community_chat, name='community_chat'),
    # path('ask', views.ask_question, name='ask_question'),
    # path('answer/<int:question_id>', views.answer_question, name='answer_question'),
    # path('comment/<int:answer_id>', views.comment_answer, name='comment_answer'),
    # path('roadmap', views.roadmap, name='roadmap'),
    # path("talkpdf1", talkpdf1, name="talkpdf1"),
    # path("category", category, name="category"),
    # path("personalcourse", personalcourse, name="personalcourse"),
    # path("compiler", compiler, name="compiler"),
    # path("ar", ar, name="ar"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)