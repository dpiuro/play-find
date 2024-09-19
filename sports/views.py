from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import View

from .models import Training, Sport, Field


User = get_user_model()

class TrainingListView(generic.ListView):
    model = Training
    template_name = "training/training_list.html"
    context_object_name = "trainings"


@method_decorator(login_required, name='dispatch')
class TrainingCreateView(generic.CreateView):
    model = Training
    fields = ['field', 'sport', 'datetime']
    template_name = "training/training_form.html"
    success_url = "/"

    def form_valid(self, form):
        # Зберігаємо форму, але не коммітимо
        self.object = form.save(commit=False)
        self.object.save()

        # Додаємо користувача, який створив подію, до учасників
        self.object.participants.add(self.request.user)

        return super().form_valid(form)


class TrainingUpdateView(generic.UpdateView):
    model = Training
    fields = ['field', 'sport', 'datetime']
    template_name = "training/training_form.html"
    success_url = "/"

class TrainingDeleteView(generic.DeleteView):
    model = Training
    template_name = "training/training_confirm_delete.html"
    success_url = "/"


class ToggleSubscriptionView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # Отримуємо тренування за допомогою його primary key (pk)
        training = get_object_or_404(Training, pk=pk)

        # Отримуємо користувача з request
        user = request.user

        # Перевіряємо, чи користувач вже підписаний
        if user in training.participants.all():
            training.participants.remove(user)  # Видаляємо користувача
        else:
            training.participants.add(user)  # Додаємо користувача

        # Перенаправляємо на список тренувань після виконання дії
        return redirect('training-list')

class FieldListView(generic.ListView):
    model = Field
    template_name = "field/field_list.html"
    context_object_name = "fields"


class FieldCreateView(generic.CreateView):
    model = Field
    fields = ['name', 'location', 'sports']
    template_name = "field/field_form.html"
    success_url = "/fields/"


class FieldUpdateView(generic.UpdateView):
    model = Field
    fields = ['name', 'location', 'sports']
    template_name = "field/field_form.html"
    success_url = "/fields/"


class FieldDeleteView(generic.DeleteView):
    model = Field
    template_name = "field/field_confirm_delete.html"
    success_url = "/fields/"


class SportListView(generic.ListView):
    model = Sport
    template_name = "sport/sport_list.html"
    context_object_name = "sports"

# Створення виду спорту
class SportCreateView(generic.CreateView):
    model = Sport
    fields = ['name']
    template_name = "sport/sport_form.html"
    success_url = reverse_lazy('sport-list')

# Оновлення виду спорту
class SportUpdateView(generic.UpdateView):
    model = Sport
    fields = ['name']
    template_name = "sport/sport_form.html"
    success_url = reverse_lazy('sport-list')

# Видалення виду спорту
class SportDeleteView(generic.DeleteView):
    model = Sport
    template_name = "sport/sport_confirm_delete.html"
    success_url = reverse_lazy('sport-list')

def home(request):
    return render(request, 'home.html')
