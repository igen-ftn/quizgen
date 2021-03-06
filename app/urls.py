from django.conf.urls import url
from app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^quiz/$', views.quizzes, name='quizzes'),
    url(r'^quiz/(?P<quiz_id>\d+)/$', views.quiz, name='quiz'),
    url(r'^survey/$', views.surveys, name='surveys'),
    url(r'^survey/(?P<survey_id>\d+)/$', views.survey, name='survey'),
    url(r'^new/$', views.new, name='new'),
    url(r'^new_quiz/$', views.new_quiz, name='new_quiz'),
    url(r'^new_survey/$', views.new_survey, name='new_survey'),
    url(r'^submit_quiz/$', views.submit_quiz, name='submit_quiz'),
    url(r'^submit_survey/$', views.submit_survey, name='submit_survey'),
    url(r'^quiz_statistic/(?P<quiz_id>\d+)/$', views.quiz_statistic, name='quiz_statistic'),
    url(r'^survey_statistic/(?P<survey_id>\d+)/$', views.survey_statistic, name='survey_statistic'),
    url(r'^quiz_results/(?P<quiz_id>\d+)/$', views.quiz_results, name='quiz_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)