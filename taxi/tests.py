from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class DriverViewsTest(TestCase):
    def test_driver_creation_form_valid_license(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "validuser",
                "password1": "Validpass123!",
                "password2": "Validpass123!",
                "license_number": "XYZ67890",  # Unique license number
            },
        )
        if response.status_code != 302:
            print("Form errors:", response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="validuser").exists())

    def test_driver_creation_form_invalid_license(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "invaliduser",
                "password1": "invalidpass123",
                "password2": "invalidpass123",
                "license_number": "bad123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "License number must be 8 characters: first 3 uppercase letters, last 5 digits.",
        )

    def setUp(self):
        self.driver_profile = get_user_model().objects.create_user(
            username="testuser", password="testpass123", license_number="ABC12345"
        )
        self.user = self.driver_profile
        self.client.login(username="testuser", password="testpass123")

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver_profile.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver_profile.license_number)  # type: ignore[attr-defined]

    def test_driver_create_view_with_valid_license(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "newuser",
                "password1": "newpass123",
                "password2": "newpass123",
                "license_number": "DEF67890",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    def test_driver_create_view_with_invalid_license(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "baduser",
                "password1": "badpass123",
                "password2": "badpass123",
                "license_number": "invalid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "License number must be 8 characters: first 3 uppercase letters, last 5 digits.",
        )

    def test_driver_delete_view(self):
        response = self.client.post(
            reverse("taxi:driver-delete", args=[self.driver_profile.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver_profile.pk).exists()
        )

    def test_update_driver_license_number_with_valid_data(self):
        response = self.client.post(
            reverse("taxi:driver-license-update", args=[self.driver_profile.pk]),
            {"license_number": "XYZ12345"},
        )
        self.assertEqual(response.status_code, 302)
        self.driver_profile.refresh_from_db()
        self.assertEqual(self.driver_profile.license_number, "XYZ12345")  # type: ignore[attr-defined]

    def test_update_driver_license_number_with_not_valid_data(self):
        response = self.client.post(
            reverse("taxi:driver-license-update", args=[self.driver_profile.pk]),
            {"license_number": "invalid"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "License number must be 8 characters: first 3 uppercase letters, last 5 digits.",
        )
