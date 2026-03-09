from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(regex="[A-Z]{3}[0-9]{5}"),
            MaxLengthValidator(8)
        ]
    )

    class Meta:
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number",))


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(8),
            RegexValidator(regex=r"[A-Z]{3}[0-9]{5}"),
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )
