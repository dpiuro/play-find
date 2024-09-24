from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Training


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "age", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['field', 'sport', 'datetime']
        widgets = {
            'datetime': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'YYYY-MM-DD HH:MM',
                    'class': 'form-control',
                }
            ),
        }
