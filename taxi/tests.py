from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from .models import Car, Manufacturer


class DriverWorkflowTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="reader", license_number="ABC12345"
        )
        self.other = get_user_model().objects.create_user(
            username="other", license_number="DEF12345"
        )
        self.car = Car.objects.create(
            model="Example",
            manufacturer=Manufacturer.objects.create(
                name="Example", country="US"
            ),
        )
        self.car.drivers.add(self.other)
        self.client.force_login(self.driver)

    def creation_data(self, **kwargs):
        return {
            "username": "newdriver",
            "first_name": "New", "last_name": "Driver",
            "license_number": "XYZ12345",
            "password1": "Unusual-password-8274",
            "password2": "Unusual-password-8274",
            **kwargs,
        }

    def test_creation_hashes_password_and_saves_names(self):
        response = self.client.post(
            reverse("taxi:driver-create"), self.creation_data()
        )
        driver = get_user_model().objects.get(username="newdriver")
        self.assertRedirects(response, driver.get_absolute_url())
        self.assertTrue(driver.check_password("Unusual-password-8274"))
        self.assertEqual(
            (driver.first_name, driver.last_name), ("New", "Driver")
        )

    def test_license_validation_on_both_forms(self):
        for value in ("abc12345", "AB123456", "ABCD1234", "ABC1234",
                      "ABC123456", "ÄBC12345", "ABC١٢٣٤٥"):
            with self.subTest(value=value):
                self.assertFalse(DriverCreationForm(
                    data=self.creation_data(license_number=value)
                ).is_valid())
                self.assertFalse(DriverLicenseUpdateForm(
                    data={"license_number": value}
                ).is_valid())

    def test_duplicate_license_and_password_mismatch_are_rejected(self):
        self.assertFalse(DriverCreationForm(data=self.creation_data(
            license_number=self.driver.license_number
        )).is_valid())
        self.assertFalse(DriverCreationForm(data=self.creation_data(
            password2="different-password"
        )).is_valid())

    def test_update_only_changes_license(self):
        response = self.client.post(reverse(
            "taxi:driver-update", args=[self.driver.pk]
        ), {"license_number": "XYZ54321", "is_staff": True,
            "username": "hacked"})
        self.assertRedirects(response, self.driver.get_absolute_url())
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "XYZ54321")
        self.assertEqual(self.driver.username, "reader")
        self.assertFalse(self.driver.is_staff)

    def test_delete_confirmation_and_post(self):
        url = reverse("taxi:driver-delete", args=[self.other.pk])
        response = self.client.get(url)
        self.assertContains(
            response,
            f'<a href="{self.other.get_absolute_url()}" '
            'class="btn btn-secondary">Cancel</a>',
            html=True,
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.other.pk).exists()
        )
        self.assertRedirects(
            self.client.post(url), reverse("taxi:driver-list")
        )
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())
        self.assertFalse(self.car.drivers.exists())

    def test_assignment_changes_only_current_user_and_is_post_only(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        detail = reverse("taxi:car-detail", args=[self.car.pk])
        self.assertContains(self.client.get(detail), "Assign me to this car")
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(
            self.client.post(url, {"user": self.other.pk}), detail
        )
        self.assertContains(
            self.client.get(detail), "Delete me from this car"
        )
        self.assertEqual(
            set(self.car.drivers.all()), {self.driver, self.other}
        )
        self.client.post(url)
        self.assertEqual(list(self.car.drivers.all()), [self.other])

    def test_assignment_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.driver)
        response = client.post(reverse(
            "taxi:toggle-car-assign", args=[self.car.pk]
        ))
        self.assertEqual(response.status_code, 403)

    def test_mutation_views_require_authentication(self):
        self.client.logout()
        for name, args in (
            ("driver-create", []), ("driver-update", [self.other.pk]),
            ("driver-delete", [self.other.pk]),
            ("toggle-car-assign", [self.car.pk]),
        ):
            url = reverse(f"taxi:{name}", args=args)
            for method in (self.client.get, self.client.post):
                with self.subTest(name=name, method=method.__name__):
                    self.assertEqual(method(url).status_code, 302)

    def test_checkbox_form_preserves_assignments(self):
        form = CarForm(instance=self.car)
        self.assertIn(self.other.pk, form["drivers"].value())
        response = self.client.get(reverse("taxi:car-create"))
        self.assertContains(response, 'type="checkbox"')
