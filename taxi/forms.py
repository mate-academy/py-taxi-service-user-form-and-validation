from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db.models.lookups import Regex
from django.shortcuts import redirect

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$", message="Invalid license number"
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ["license_number"]

    def form_valid(self):
        return redirect(self.get_success_url())


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
