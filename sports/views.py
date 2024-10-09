from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView

from sports.forms import CustomUserCreationForm, TrainingForm
from sports.mixins import UserPermissionMixin, UserStatusMixin
from sports.models import Training, Sport, Field


class TrainingListView(LoginRequiredMixin, generic.ListView):
    model = Training
    template_name = "training/training_list.html"
    context_object_name = "trainings"
    paginate_by = 5
    login_url = "login"

    def get_queryset(self):
        return (
            Training.objects.select_related("field", "sport")
            .prefetch_related("participants")
            .order_by("datetime")
        )


class TrainingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "training/training_form.html"
    success_url = reverse_lazy("training-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        try:
            form.instance.full_clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        training = form.save()
        training.participants.add(self.request.user)
        return super().form_valid(form)


class TrainingUpdateView(
    LoginRequiredMixin,
    UserPermissionMixin,
    generic.UpdateView
):
    model = Training
    fields = ["field", "sport", "datetime"]
    template_name = "training/training_form.html"
    success_url = "/"
    login_url = "login"


class TrainingDeleteView(
    LoginRequiredMixin,
    UserPermissionMixin,
    generic.DeleteView
):
    model = Training
    template_name = "training/training_confirm_delete.html"
    success_url = reverse_lazy("training-list")


class TrainingDetailView(DetailView):
    model = Training
    template_name = "training/training_detail.html"
    context_object_name = "training"


class FieldListView(UserStatusMixin, generic.ListView):
    model = Field
    template_name = "field/field_list.html"
    context_object_name = "fields"
    paginate_by = 5

    def get_queryset(self):
        return Field.objects.order_by("name")


class FieldCreateView(generic.CreateView):
    model = Field
    fields = ["name", "location", "sports"]
    template_name = "field/field_form.html"
    success_url = reverse_lazy("field_list")


class FieldUpdateView(generic.UpdateView):
    model = Field
    fields = ["name", "location", "sports"]
    template_name = "field/field_form.html"
    success_url = reverse_lazy("field_list")


class FieldDeleteView(generic.DeleteView):
    model = Field
    template_name = "field/field_confirm_delete.html"
    success_url = reverse_lazy("field_list")


class FieldDetailView(generic.DetailView):
    model = Field
    template_name = "field/field_detail.html"
    context_object_name = "field"

    def get_queryset(self):
        return Field.objects.prefetch_related("sports")


class SportListView(UserStatusMixin, generic.ListView):
    model = Sport
    template_name = "sport/sport_list.html"
    context_object_name = "sports"
    paginate_by = 5

    def get_queryset(self):
        return Sport.objects.order_by("name")


class SportCreateView(generic.CreateView):
    model = Sport
    fields = ["name"]
    template_name = "sport/sport_form.html"
    success_url = reverse_lazy("sport-list")


class SportUpdateView(generic.UpdateView):
    model = Sport
    fields = ["name"]
    template_name = "sport/sport_form.html"
    success_url = reverse_lazy("sport-list")


class SportDeleteView(generic.DeleteView):
    model = Sport
    template_name = "sport/sport_confirm_delete.html"
    success_url = reverse_lazy("sport-list")


class SportDetailView(generic.DetailView):
    model = Sport
    template_name = "sport/sport_detail.html"
    context_object_name = "sport"

    def get_queryset(self):
        return Sport.objects.prefetch_related("fields")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fields"] = Field.objects.filter(sports=self.object)
        return context


def home_view(request):
    num_trainings = Training.objects.count()
    num_fields = Field.objects.count()
    num_sports = Sport.objects.count()

    context = {
        "num_trainings": num_trainings,
        "num_fields": num_fields,
        "num_sports": num_sports,
    }
    return render(request, "home.html", context)


@login_required
def toggle_training_subscription(request, pk):
    training = get_object_or_404(
        Training.objects.prefetch_related("participants"), pk=pk
    )
    user = request.user

    if user in training.participants.all():
        training.participants.remove(user)
    else:
        training.participants.add(user)

    return redirect("training-list")


def search_trainings(request):
    query = request.GET.get("q")
    trainings = (
        Training.objects.select_related("sport")
        .filter(Q(sport__name__icontains=query))
        .order_by("sport")
        if query
        else Training.objects.select_related("sport").order_by("sport")
    )
    return render(
        request,
        "training/training_list.html",
        {"trainings": trainings, "query": query}
    )


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            form = CustomUserCreationForm()
        return render(
            request,
            "registration/register.html",
            {"form": form}
        )


class CustomUserCreationView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
