from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^xiaoxue/$', views.affection, name='affection'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^projects/$', views.group_member, name='group_member'),
    url(r'^projects/finish/$', views.finish, name='finish'),
    url(r'^projects/add/$', views.add_project, name='add_project'),
    url(r'^projects/quit/$', views.quit_project, name='quit_project'),
    url(r'^personal/$', views.personal_project, name='personal_project'),
    url(r'^register/$', views.register_with_project, name='register_with_project'),
    url(r'^unregister/$', views.unregister, name='unregister'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

]
