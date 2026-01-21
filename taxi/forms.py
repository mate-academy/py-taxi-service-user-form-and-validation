from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class LicenseNumberValidationMixin:
    def clean_license_number(self) -> str:
        value = self.cleaned_data["license_number"]
        if len(value) != 8:
            raise ValidationError(
                "The length of the field must be exactly 8 characters"
            )
        part1, part2 = value[:3], value[3:]
        if not part1.isalpha() or not part1.isupper():
            raise ValidationError(
                "First three characters must be uppercase letters"
            )
        if not part2.isdecimal():
            raise ValidationError(
                "Last five characters must be decimal digits"
            )
        return value


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
