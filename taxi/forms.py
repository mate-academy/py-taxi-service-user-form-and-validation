from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "first_name", "last_name", )


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta:
        model = Driver
        fields = ("license_number", )



