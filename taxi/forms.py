from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        ln = self.cleaned_data["license_number"]
        if len(ln) != 8:
            raise ValidationError(
                "Ensure that license length is correct"
            )
        if not ln[0:3].isalpha():
            raise ValidationError("First characters must be letters")

        if ln[0:3].upper() != ln[0:3]:
            raise ValidationError(
                "Ensure that license letters is correct"
            )
        if not ln[3:].isdigit():
            raise ValidationError(
                "Ensure that license digits is correct"
            )
        return ln


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
