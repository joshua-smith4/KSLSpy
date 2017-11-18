from django.conf.urls import url

from . import views

app_name = 'KSLSpyViewer'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^validateLogin/$', views.validateLogin, name='validateLogin'),
]