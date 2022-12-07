from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car
from django import forms


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username", "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "must be only 8 characters"
            )
        if not license_number[:3].isalpha():
            raise ValidationError(
                "First 3 elements, must be only letters"
            )
        if license_number[:3].islower():
            raise ValidationError(
                "First thee element must be in uppercase"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "last 5 elements must be only digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
