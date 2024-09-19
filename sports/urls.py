from django.contrib import admin
from django.urls import path, include  # Додаємо include

from sports import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trainings/', views.TrainingListView.as_view(), name='training-list'),
    path('trainings/create/', views.TrainingCreateView.as_view(), name='training-create'),
    path('trainings/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training-update'),
    path('trainings/<int:pk>/delete/', views.TrainingDeleteView.as_view(), name='training-delete'),
    path('trainings/<int:pk>/subscribe/', views.toggle_training_subscription, name='training-subscribe'),
    path('fields/', views.FieldListView.as_view(), name='field-list'),
    path('sport/', views.SportListView.as_view(), name='sport-list'),
]