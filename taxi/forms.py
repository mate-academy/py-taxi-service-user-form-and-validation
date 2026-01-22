from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator


from taxi.models import Driver, Car
from django import forms


class DriverLicenseUpdateForm(forms.ModelForm):
    LEN_CHARACTERS = 8
    license_number = forms.CharField(

        validators=[
            MinLengthValidator(LEN_CHARACTERS),
            MaxLengthValidator(LEN_CHARACTERS),
        ]
    )

    class Meta:
        model = Driver
        fields = (
            "license_number",
        )

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        if (not license_number[0:3].isalpha()
                or not license_number[0:3].isupper()):
            raise forms.ValidationError(
                "First 3 characters are uppercase letters."
            )
        elif not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters are digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    LEN_CHARACTERS = 8
    license_number = forms.CharField(

        validators=[
            MinLengthValidator(LEN_CHARACTERS),
            MaxLengthValidator(LEN_CHARACTERS),
        ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
