from django.contrib.auth.forms import UserCreationForm
from django import forms

from sports.models import User, Training, Sport, Field


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "age", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TrainingForm(forms.ModelForm):
    field = forms.ModelChoiceField(
        queryset=Field.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Training
        fields = ["field", "sport", "datetime"]
        widgets = {
            "datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "placeholder": "YYYY-MM-DD HH:MM",
                    "class": "form-control",
                }
            ),
        }
