from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelMultipleChoiceField, ModelChoiceField
from django.forms.widgets import TextInput, CheckboxSelectMultiple, HiddenInput

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]
        widgets = {
            "license_number": TextInput(attrs={"class": "form-control"}),
        }


class CarCreateForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=Driver.objects,
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarDriverToggleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        car = self.instance
        if car.drivers.filter(id=self.user.id).exists():
            car.drivers.remove(self.user)
        else:
            car.drivers.add(self.user)

        return car

    class Meta:
        model = Car
        fields = []
