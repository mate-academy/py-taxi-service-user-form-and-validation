from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self, length=8):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != length:
            raise ValidationError(
                f"Ensure that value is = {length}"
            )
        if not license_number[:3].isalpha() \
                or not license_number[:3].isupper():
            raise ValidationError(
                "Expect: first 3 characters are uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Expect: last 5 characters are digits"
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
