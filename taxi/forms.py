from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must consist 8 symbols")
        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
                or not license_number[3:].isdigit()
        ):
            raise ValidationError(
                "The license number must contain the first 3 alphabet"
                " characters in uppercase,"
                " and the last 5 characters as numbers"
            )
        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
            "license_number",
            "first_name",
            "last_name",
            "is_staff",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
