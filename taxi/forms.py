from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, RegexValidator
from django import forms
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8
    LICENSE_PATTERN = r"^[A-Z]{3}\d{5}$"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["license_number"] = forms.CharField(
            max_length=self.LICENSE_LENGTH,
            required=True,
            validators=[
                MaxLengthValidator(self.LICENSE_LENGTH),
                RegexValidator(
                    regex=self.LICENSE_PATTERN,
                    message="License number must consist of 3 "
                            "uppercase letters followed by"
                            " 5 digits (e.g. ABC12345)"
                )
            ]
        )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
