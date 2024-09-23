# Generated by Django 5.1.1 on 2024-09-19 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sports", "0002_training_creator_alter_training_field_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="training",
            name="creator",
        ),
        migrations.AlterField(
            model_name="training",
            name="field",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="field_trainings",
                to="sports.field",
            ),
        ),
        migrations.AlterField(
            model_name="training",
            name="sport",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sport_trainings",
                to="sports.sport",
            ),
        ),
    ]
