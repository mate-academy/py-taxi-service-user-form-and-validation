from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class DriverCreationForm(UserCreationForm):

    license_validator = RegexValidator(
        regex=r"^[A-Z]{3}\d{5}$",
        message="""License must contain 3 uppercase letters
        followed by 5 digits."""
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        self.license_validator(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):

    license_validator = RegexValidator(
        regex=r"^[A-Z]{3}\d{5}$",
        message="""License must contain 3 uppercase letters
        followed by 5 digits."""
    )

    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        self.license_validator(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,)

    class Meta:
        model = Car
        fields = "__all__"
