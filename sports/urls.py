from django.urls import path, include
from sports import views
from sports.views import toggle_training_subscription, CustomUserCreationView

urlpatterns = [
    path('', views.home, name='home'),  # Домашня сторінка
    path('trainings/', views.TrainingListView.as_view(), name='training-list'),  # Список тренувань
    path('trainings/create/', views.TrainingCreateView.as_view(), name='training-create'),  # Створити тренування
    path('trainings/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training-update'),  # Оновити тренування
    path('trainings/<int:pk>/delete/', views.TrainingDeleteView.as_view(), name='training-delete'),  # Видалити тренування
    path('trainings/<int:pk>/subscribe/', toggle_training_subscription, name='training-subscribe'), # Підписка на тренування

    path('fields/', views.FieldListView.as_view(), name='field-list'),  # Список полів
    path('fields/create/', views.FieldCreateView.as_view(), name='field-create'),  # Створити поле
    path('fields/<int:pk>/update/', views.FieldUpdateView.as_view(), name='field-update'),  # Оновити поле
    path('fields/<int:pk>/delete/', views.FieldDeleteView.as_view(), name='field-delete'),  # Видалити поле

    path('sport/', views.SportListView.as_view(), name='sport-list'),
    path('sport/create/', views.SportCreateView.as_view(), name='sport-create'),
    path('sport/<int:pk>/update/', views.SportUpdateView.as_view(), name='sport-update'),
    path('sport/<int:pk>/delete/', views.SportDeleteView.as_view(), name='sport-delete'),
    path('search/', views.search_trainings, name='training-search'),
    path('register/', views.register, name='register'),
    path('signup/', CustomUserCreationView.as_view(), name='signup'),
]
