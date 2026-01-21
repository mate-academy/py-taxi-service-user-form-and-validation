from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from taxi.validators import license_number_validator


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email"
        )
        license_number = forms.CharField(
            required=True,
            validators=[license_number_validator]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class AssignDriverForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_car_id(self):
        car_id = self.cleaned_data["car_id"]
        if not Car.objects.filter(pk=car_id).exists():
            raise ValidationError("Car does not exist.")
        return car_id


class RemoveDriverForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_car_id(self):
        car_id = self.cleaned_data["car_id"]
        if not Car.objects.filter(pk=car_id).exists():
            raise ValidationError("Car does not exist.")
        return car_id
