from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('guide/',views.guide, name="guide"),
    
    path('datasets/<slug:slug>/', views.dataset, name="dataset"),
    path('datasets/<slug:slug>/process/', views.process, name="process"),
    path('datasets/<slug:slug>/edit/', views.UpdateDatasetView.as_view(), name="edit"),
    path('datasets/<slug:slug>/delete/', views.DeleteDatasetView.as_view(), name="delete_dataset"),
    

    path('datafiles/', views.DatasetFileView.as_view(), name="datafiles"),
    path('datafiles/<slug:slug>/', views.SetupDatasetView.as_view(), name="process_datafile"),
    path('datafiles/<slug:slug>/delete/', views.DeleteDataFileView.as_view(), name="delete_datafile")
]
