from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        length_ = 8
        num_of_letters = 3

        if len(license_number) != length_:
            raise forms.ValidationError(
                f"License must be exactly {length_} characters long."
            )

        if not (license[:num_of_letters].isupper() and license[:num_of_letters].isalpha()):
            raise forms.ValidationError(
                f"First {num_of_letters} characters must be uppercase letters."
            )

        if not license[num_of_letters:].isdigit():
            raise forms.ValidationError(
                f"Last {length_ - num_of_letters} characters must be digits."
            )

        return license


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
