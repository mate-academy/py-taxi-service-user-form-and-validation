from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple
from django.forms.models import ModelForm, ModelMultipleChoiceField

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", "first_name", "last_name")

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License number must be "
                                  "exactly 8 characters long.")

        prefix = license_number[:3]
        suffix = license_number[3:]

        if not (prefix.isalpha() and prefix.isupper()):
            raise ValidationError("The first 3 characters must"
                                  " be uppercase letters.")

        if not suffix.isdigit():
            raise ValidationError("The last 5 characters"
                                  " must be digits.")

        qs = Driver.objects.filter(license_number=license_number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Driver with this "
                                  "License number already exists.")

        return license_number


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = ["model", "drivers"]
