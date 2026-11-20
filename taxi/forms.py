from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Car


class CleanLicenseMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("Licence number"
                                  " must be 8 characters long")
        if not license_number[: 3].isupper():
            raise ValidationError("Licence number must have"
                                  " first 3 characters is apper case")
        if not license_number[: 3].isalpha():
            raise ValidationError("Licence number must"
                                  " have first 3 characters is letters"
                                  )
        if not license_number[3:].isdigit():
            raise ValidationError("last 5 characters only digits")
        return license_number


class DriverLicenseUpdateForm(CleanLicenseMixin, forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class DriverCreationForm(CleanLicenseMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name" , "license_number",
        )


class CarForms(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
