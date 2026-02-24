from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm

from taxi.models import  Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[RegexValidator("^[A-Z]{3}\d{5}$", "License must be 3 uppercase letters followed by 5 digits")]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "license_number",)


class DriverLicenseUpdateForm(ModelForm):
    license_number = forms.CharField(
        validators=[RegexValidator("^[A-Z]{3}\d{5}$", "Invalid license")]
    )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (get_user_model().objects
                .filter(license_number=license_number)
                .exclude(pk=self.instance.pk)
                .exists()):
            raise forms.ValidationError("This license number already exists")
        return license_number

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }


class CarUpdateDriversForm(ModelForm):
    class Meta:
        model = Car
        fields = ("drivers",)
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
