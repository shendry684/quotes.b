from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('addquote', views.addquote),
    path('dashboard', views.dashboard), 
    path('login', views.login),
    path('logout', views.logout),
    path('showquote/<id>', views.showquote),
    path('favorite/<id>', views.favorite),
    path('unfavorite/<id>', views.unfavorite),
    path('delete/<id>', views.delete),
    path('processquote', views.processquote),
    path('login', views.login),
    path('logout', views.logout),
      
]
