from django.forms import (ModelForm,
                          ModelMultipleChoiceField,
                          CheckboxSelectMultiple)
from django.contrib.auth import forms, get_user_model

from taxi.models import Driver, Car


class DriverCreationForm(forms.UserCreationForm):

    class Meta(forms.UserCreationForm.Meta):
        model = Driver
        fields = forms.UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(ModelForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Driver
        fields = ("license_number", )


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
