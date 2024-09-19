from django.db import models
from django.contrib.auth.models import AbstractUser


class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sports_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sports_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Field (models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    sports = models.ManyToManyField(Sport, related_name="fields")

    def __str__(self):
        return self.name


class Training(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_trainings")
    participants = models.ManyToManyField(User, related_name="participant_trainings", blank=True)


    def __str__(self):
        return f"Training at {self.field.name} on {self.datetime} for {self.sport}"
