from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver

class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("username", "password1", "password2", "license_number")