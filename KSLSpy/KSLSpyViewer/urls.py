from django.conf.urls import url

from . import views

app_name = 'KSLSpyViewer'
urlpatterns = [
    url(r'^$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^validateLogin/$', views.validateLogin, name='validateLogin'),
]