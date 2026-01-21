from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "license_number", "first_name", "last_name",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")


class AddCarForm(forms.ModelForm):
    assign_me_to_this_car = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", })
    )
    remove_me_from_this_car = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", })
    )

    class Meta:
        model = Car
        fields = ("assign_me_to_this_car", "remove_me_from_this_car")
