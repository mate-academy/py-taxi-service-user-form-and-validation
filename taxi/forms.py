from django import forms
from taxi.models import Car
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class DriverBaseForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must contain 8 characters")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[3:].isnumeric():
            raise ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreateForm(UserCreationForm, DriverBaseForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "license_number",
            "username",
            "password",
            "first_name",
            "last_name",
            "email"
        )


class DriverLicenseUpdateForm(DriverBaseForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
