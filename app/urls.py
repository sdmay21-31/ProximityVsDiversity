from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process/', views.process, name="process"),
    path('databases/', views.databases, name="databases"),
    path('databases/<slug:database>/attributes/', views.attributes , name="attributes"),
    path('add/', views.add_dataset, name="add_dataset"),
    path('add/<slug:filename>/', views.SetupDatasetView.as_view(), name="add_dataset"),

]
