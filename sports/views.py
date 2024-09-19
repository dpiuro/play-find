from audioop import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sports.models import Training


class TrainingListView(ListView):
    model = Training
    template_name = "training-list.html"
    context_object_name = "training-list"
    paginate_by = 5


class TrainingCreateView(CreateView):
    model = Training
    fields = ["field", "sport", "date", "time", "participants"],
    template_name = "training-form.html"
    success_url = reverse_lazy("training_list")


class TrainingUpdateView(UpdateView):
    model = Training
    fields = ["field", "sport", "date", "time", "participants"]
    template_name = "training-form.html"
    success_url = reverse_lazy("training-list")


class TrainingDeleteView(DeleteView):
    model = Training
    template_name = "training_confirm_delete.html"
    success_url = reverse_lazy("training-list")


def subscribe_to_training(request, pk) -> HttpResponse:
    training = get_object_or_404(Training, pk=pk)
    training.participants.add(request.user)
    return HttpResponseRedirect(reverse_lazy("training-list"))
