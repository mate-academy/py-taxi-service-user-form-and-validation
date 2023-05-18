from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car
from django.contrib.auth.forms import UserCreationForm
from django import forms


class DriverLicenseUpdateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver

        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("length must be equal 8 simbols'")

        se = f"{license_number[0]}{license_number[1]}{license_number[2]}"
        no = f"{license_number[3]}{license_number[4]}{license_number[5]}{license_number[6]}{license_number[7]}"

        if not se.isalpha() or se.upper() != se:
            raise ValidationError("first three simbols must be latin, upper, letters")

        try:
            int(no)
        except ValueError:
            raise ValidationError("last five simbols must be numeric")

        return license_number


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
