from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Car

User = get_user_model()


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        import re
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "Numer prawa jazdy musi mieć dokładnie 8 znaków: "
                "3 wielkie litery i 5 cyfr (np. 'ABC12345')."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        import re
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "Numer prawa jazdy musi mieć dokładnie 8 znaków: "
                "3 wielkie litery i 5 cyfr (np. 'ABC12345')."
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
