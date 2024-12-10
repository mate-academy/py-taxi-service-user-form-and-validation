from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number")


class CarCreateForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": CheckboxSelectMultiple}
