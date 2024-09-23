from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Training, Sport, Field

User = get_user_model()


class TrainingTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.sport = Sport.objects.create(name="Football")
        self.field = Field.objects.create(name="Main Field", location="Center")
        self.field.sports.add(self.sport)
        self.training = Training.objects.create(
            field=self.field, sport=self.sport, datetime="2024-09-25 10:00"
        )
        self.client.login(username="testuser", password="password123")

    def test_create_training(self):
        form_data = {
            "field": self.field.id,
            "sport": self.sport.id,
            "datetime": "2024-09-25 12:00",
        }
        response = self.client.post(reverse("training-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Training.objects.filter(datetime="2024-09-25 12:00").exists())

    def test_update_training_valid_data(self):
        form_data = {
            "field": self.field.id,
            "sport": self.sport.id,
            "datetime": "2024-09-26 10:00",
        }
        response = self.client.post(
            reverse("training-update", kwargs={"pk": self.training.pk}), data=form_data
        )
        self.training.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.training.datetime.strftime("%Y-%m-%d %H:%M"), "2024-09-26 10:00"
        )

    def test_delete_training(self):
        response = self.client.post(
            reverse("training-delete", kwargs={"pk": self.training.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Training.objects.filter(id=self.training.id).exists())

    def test_search_training(self):
        response = self.client.get(reverse("training-list") + "?q=Football")
        self.assertContains(response, "Football")
        self.assertContains(response, "Main Field")


class UserRegistrationTestCase(TestCase):

    def test_user_registration(self):
        form_data = {
            "username": "newuser",
            "password1": "Password123!",
            "password2": "Password123!",
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class SportModelTestCase(TestCase):

    def setUp(self):
        self.sport = Sport.objects.create(name="Volleyball")

    def test_unique_sport_name(self):
        with self.assertRaises(Exception):
            Sport.objects.create(name="Volleyball")


class FieldCreationTest(TestCase):
    def setUp(self):
        self.sport = Sport.objects.create(name="Basketball")

    def test_create_field(self):
        field = Field.objects.create(name="Basketball Court", location="Downtown")
        field.sports.add(self.sport)

        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(field.name, "Basketball Court")
        self.assertEqual(field.location, "Downtown")
        self.assertIn(self.sport, field.sports.all())
