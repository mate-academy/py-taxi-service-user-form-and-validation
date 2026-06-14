from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


User = get_user_model()


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not license_number:
            return license_number

        if len(license_number) != 8:
            raise ValidationError("number must be 8 characters long!")

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("first 3 characters must be"
                                  " UPPERCASE and must be letters!")

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits!")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not license_number:
            return license_number

        if len(license_number) != 8:
            raise ValidationError("number must be 8 characters long!")

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise (ValidationError
                   ("first 3 characters must"
                    " be UPPERCASE and must be letters!"))

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits!")

        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
