from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields +
                  ("license_number", "first_name", "last_name", ))

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError("License number must "
                                  "be 8 characters long")
        if not (license_number[:3].isalpha() and
                license_number[:3].isupper()):
            raise ValidationError("License number must "
                                  "begin with 3 big letters")
        if not license_number[3:].isdigit():
            raise ValidationError("License number must "
                                  "end with 5 digits")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError("License number must "
                                  "be 8 characters long")
        if not (license_number[:3].isalpha() and
                license_number[:3].isupper()):
            raise ValidationError("License number must "
                                  "begin with 3 big letters")
        if not license_number[3:].isdigit():
            raise ValidationError("License number must "
                                  "end with 5 digits")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
