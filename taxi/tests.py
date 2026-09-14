from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarForm, DriverCreationForm
from taxi.models import Car, Manufacturer


class DriverFormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "test.driver",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "ABC12345",
            "password1": "password123!",
            "password2": "password123!",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "test.driver",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "invalid",
            "password1": "password123!",
            "password2": "password123!",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormAndViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Prius", manufacturer=self.manufacturer
        )

    def test_car_form_has_checkboxes_widget(self):
        form = CarForm()
        self.assertEqual(
            form.fields["drivers"].widget.__class__.__name__,
            "CheckboxSelectMultiple",
        )

    def test_toggle_assign_user_to_car(self):
        self.assertNotIn(self.user, self.car.drivers.all())
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.car.drivers.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.car.drivers.all())

    def test_driver_create_view(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("taxi:driver-create"),
            data={
                "username": "new.driver",
                "first_name": "New",
                "last_name": "Driver",
                "license_number": "NEW12345",
                "password1": "1qazcde3!",
                "password2": "1qazcde3!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="new.driver").exists()
        )
