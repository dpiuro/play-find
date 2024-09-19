from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Training, Sport, Field


class TrainingListView(generic.ListView):
    model = Training
    template_name = "training/training_list.html"
    context_object_name = "trainings"

class TrainingCreateView(generic.CreateView):
    model = Training
    fields = ['field', 'organizer', 'date', 'time']
    template_name = "training/training_form.html"
    success_url = "/"

class TrainingUpdateView(generic.UpdateView):
    model = Training
    fields = ['field', 'sport', 'datetime']
    template_name = "training/training_form.html"
    success_url = "/"

class TrainingDeleteView(generic.DeleteView):
    model = Training
    template_name = "training/training_confirm_delete.html"
    success_url = "/"



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
    queryset = Sport.objects.all()

def home(request):
    return render(request, 'home.html')


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Training

@login_required
def toggle_training_subscription(request, pk):
    training = get_object_or_404(Training, pk=pk)

    # Отримуємо об'єкт User безпосередньо
    user = User.objects.get(pk=request.user.pk)

    # Перевіряємо, чи користувач вже є учасником тренування
    if user in training.participants.all():
        training.participants.remove(user)  # Відписати користувача
    else:
        training.participants.add(user)  # Підписати користувача

    return redirect('training-list')
