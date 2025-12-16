from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import (ModelForm,
                          ModelMultipleChoiceField,
                          CheckboxSelectMultiple)

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(ModelForm):
    class Meta():
        model = get_user_model()
        fields = (
            "license_number",
        )

    def clean_license_number(self):
        license_data = self.cleaned_data["license_number"]
        if len(license_data) != 8:
            raise ValidationError(
                "Ensure that license number has 8 symbols"
            )
        if (
            not license_data[0].isupper()
            or not license_data[1].isupper()
            or not license_data[2].isupper()
        ):
            raise ValidationError(
                "Ensure that first 3 characters are upppercase"
            )

        for char in license_data[3:]:
            if not char.isdigit():
                raise ValidationError(
                    "Ensure that last 5 characters are digit"
                )

        return license_data


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta():
        model = Car
        fields = "__all__"
