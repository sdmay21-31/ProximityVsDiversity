from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('datasets/<slug:slug>/', views.dataset, name="dataset"),
    path('datasets/<slug:slug>/process/', views.process, name="process"),
    path('add/<slug:slug>/edit/', views.UpdateDatasetView.as_view(), name="edit"),

    path('guide/',views.guide, name="guide"),

    path('add/', views.add_dataset, name="add_dataset"),
    path('add/<filename>/', views.SetupDatasetView.as_view(), name="add_dataset"),
    path('upload/', views.upload, name="upload"),
]
