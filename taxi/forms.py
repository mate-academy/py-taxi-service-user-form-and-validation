from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple

from taxi.models import Car


class CleanLicenseMixin:
    def clean_license_number(self):
        driver_license = self.cleaned_data["license_number"]
        if len(driver_license) != 8:
            raise ValidationError("The license must contain 8 symbols")
        if (not driver_license[:3].isupper()
                or not driver_license[:3].isalpha()):
            raise ValidationError(
                "First three symbols must be 3 uppercased letters"
            )
        if not driver_license[3:].isdigit():
            raise ValidationError("Last five symbols must be digits")
        return driver_license


class DriverCreationForm(UserCreationForm, CleanLicenseMixin):
    password_len = 8

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, CleanLicenseMixin):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
