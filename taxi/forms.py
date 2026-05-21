from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseValidateMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("Value should be 8 length")

        first_3 = license_number[:3]
        if not first_3.isalpha() or not first_3.isupper():
            raise ValidationError("First 3 symbols should be upper")

        last_5 = license_number[3:]
        if len(last_5) != 5 or not last_5.isdigit():
            raise ValidationError("Last 5 symbols should be digit")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(DriverLicenseValidateMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreateForm(DriverLicenseValidateMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)
