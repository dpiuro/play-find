from django.contrib import admin
from django.urls import path, include  # Додаємо include

from sports import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trainings/', views.TrainingListView.as_view(), name='training-list'),
    path('trainings/create/', views.TrainingCreateView.as_view(), name='training-create'),
    path('fields/', views.FieldListView.as_view(), name='field-list'),
    path('sport/', views.SportListView.as_view(), name='sport-list'),
]