from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Car, Manufacturer


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("TES12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("TES1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("TE123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("TEST2345").is_valid())


class DriverViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self):
        driver = get_user_model().objects.create(
            username="not_admin.user",
            license_number="NOT12345",
            first_name="Not Admin",
            last_name="User",
            password="1qazcde3",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )

    def test_create_driver_with_valid_license(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            data={
                "username": "new.driver",
                "first_name": "New",
                "last_name": "Driver",
                "license_number": "NEW12345",
                "password1": "Y7!vPz$1QmT",
                "password2": "Y7!vPz$1QmT",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="new.driver").exists()
        )

    def test_create_driver_with_invalid_license_is_rejected(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            data={
                "username": "invalid.driver",
                "license_number": "abc12345",
                "password1": "Y7!vPz$1QmT",
                "password2": "Y7!vPz$1QmT",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="invalid.driver").exists()
        )


class CarFormAndAssignmentTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test.driver",
            license_number="TST12345",
            password="1qazcde3",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_car_driver_picker_uses_checkboxes(self):
        self.assertEqual(
            CarForm.base_fields["drivers"].widget.__class__.__name__,
            "CheckboxSelectMultiple",
        )

    def test_assign_and_remove_current_driver(self):
        assign_url = reverse(
            "taxi:car-assign-me",
            kwargs={"pk": self.car.pk},
        )
        remove_url = reverse(
            "taxi:car-remove-me",
            kwargs={"pk": self.car.pk},
        )

        assign_response = self.client.post(assign_url)
        self.assertEqual(assign_response.status_code, 302)
        self.assertTrue(self.car.drivers.filter(pk=self.driver.pk).exists())

        remove_response = self.client.post(remove_url)
        self.assertEqual(remove_response.status_code, 302)
        self.assertFalse(self.car.drivers.filter(pk=self.driver.pk).exists())

    def test_car_creation_saves_selected_drivers(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            data={
                "model": "Prius",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        car = Car.objects.get(model="Prius")
        self.assertTrue(car.drivers.filter(pk=self.driver.pk).exists())
