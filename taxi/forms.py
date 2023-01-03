from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, RegexValidator
from django import forms
from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LENGTH = 8

    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(regex="[A-Z]{3}[0-9]{5}",
                           message="License number must contain"
                                   " three uppercase letters "
                                   "followed by five numbers"),
            MaxLengthValidator(MAX_LENGTH)
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "license_number",
        )
