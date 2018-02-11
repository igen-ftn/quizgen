from django.conf.urls import url
from app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^gen/$', views.gen, name='gen'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^new/$', views.new, name='new'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)