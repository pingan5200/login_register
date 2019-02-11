from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.loginView, name='login'),
    path('register', views.registerView, name='register'),
    path('ajax_val', views.ajax_val, name='ajax_val')
]