from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import Driver, Car, Manufacturer


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class CarCreationForm(forms.ModelForm):
    assigned_drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Car
        fields = ("assigned_drivers",
                  "manufacturer",
                  "model",)

    def save(self, commit=True):
        car = super(CarCreationForm, self).save(commit=False)

        if commit:
            car.save()
            self.save_m2m()
            car.drivers.set(self.cleaned_data["assigned_drivers"])

        return car


class DriverLicenseUpdateForm(ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)
