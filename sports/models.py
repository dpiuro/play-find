from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="sports_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="sports_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Field(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    sports = models.ManyToManyField(Sport, related_name="fields")

    def __str__(self):
        return self.name


class Training(models.Model):
    field = models.ForeignKey(
        Field, related_name="field_trainings", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(
        Sport, related_name="sport_trainings", on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        User, related_name="participant_trainings", blank=True
    )
    datetime = models.DateTimeField()
    creator = models.ForeignKey(
        User, related_name="created_trainings", on_delete=models.CASCADE
    )

    def clean(self):
        overlapping_trainings = Training.objects.filter(
            field=self.field, datetime=self.datetime
        )
        if overlapping_trainings.exists():
            raise ValidationError(
                "There is already a training "
                "scheduled on this field at the same time."
            )

        if self.sport not in self.field.sports.all():
            raise ValidationError(
                f"{self.sport.name} is not supported on this field."
            )

    def __str__(self):
        return (f"Training at {self.field.name} "
                f"on {self.datetime} for {self.sport}")
