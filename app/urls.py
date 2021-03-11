from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process/', views.process, name="process"),
    path('databases/', views.databases, name="databases"),
    path('databases/<slug:database>/attributes/', views.attributes , name="attributes")
]
