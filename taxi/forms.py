from django import forms
from taxi.models import Car, Driver
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError


class LicenseValidationMixin():

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters")
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError("License number must start"
                                  "with 3 uppercase letters")
        if not license_number[3:].isdigit():
            raise ValidationError("License number must end with 5 digits")

        return license_number


class DriverLicenseCreateForm(LicenseValidationMixin, UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseValidationMixin, UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
