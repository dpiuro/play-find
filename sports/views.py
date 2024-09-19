from django.shortcuts import render
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


class FieldListView(generic.ListView):
    model = Field
    template_name = "field/field_list.html"
    context_object_name = "fields"


class SportListView(generic.ListView):
    model = Sport
    template_name = "sport/sport_list.html"
    context_object_name = "sports"
    queryset = Sport.objects.all()

def home(request):
    return render(request, 'home.html')


