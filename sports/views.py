from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import View, DetailView

from .forms import CustomUserCreationForm
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
        # Призначаємо поточного користувача як творця
        form.instance.creator = self.request.user
        response = super().form_valid(form)

        # Додаємо творця до учасників
        self.object.participants.add(self.request.user)
        return response


class TrainingUpdateView(generic.UpdateView):
    model = Training
    fields = ['field', 'sport', 'datetime']
    template_name = "training/training_form.html"
    success_url = "/"

class TrainingDeleteView(generic.DeleteView):
    model = Training
    template_name = "training/training_confirm_delete.html"
    success_url = "/"

class TrainingDetailView(DetailView):
    model = Training
    template_name = 'training/training_detail.html'
    context_object_name = 'training'


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



@login_required
def toggle_training_subscription(request, pk):
    training = get_object_or_404(Training, pk=pk)
    user = request.user

    if user in training.participants.all():
        training.participants.remove(user)  # Відписатися
    else:
        training.participants.add(user)  # Підписатися

    return redirect('training-list')

def search_trainings(request):
    query = request.GET.get('q')
    trainings = Training.objects.filter(Q(sport__name__icontains=query))
    return render(request, 'training/training_search_results.html', {'trainings': trainings})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form - CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


class CustomUserCreationView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

