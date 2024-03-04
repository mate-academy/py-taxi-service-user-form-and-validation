from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverFormMixin:

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not len(license_number) == 8:
            raise ValidationError(
                "License number must consist only of 8 characters"
            )

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class DriverCreationForm(DriverFormMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(DriverFormMixin, forms.ModelForm):
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
