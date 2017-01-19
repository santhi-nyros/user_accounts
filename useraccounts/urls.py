from django.conf.urls import url,include
from django.contrib.auth.views import password_reset
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^reg/', views.regisration, name='registration'),
	url(r'^login/', views.login, name='login'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^update/', views.updateProfile, name='update'),
	url(r'^reset_password/', views.password_reset, name='reset_password'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
]
