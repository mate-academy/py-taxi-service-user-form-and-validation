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
        license = self.cleaned_data.get("license_number")
        LENGTH = 8
        NUM_OF_LETTERS = 3

        if len(license) != LENGTH:
            raise forms.ValidationError(f"License must be exactly {LENGTH} characters long.")

        if not (license[:NUM_OF_LETTERS].isupper() and license[:NUM_OF_LETTERS].isalpha()):
            raise forms.ValidationError(f"First {NUM_OF_LETTERS} characters must be uppercase letters.")

        if not license[NUM_OF_LETTERS:].isdigit():
            raise forms.ValidationError(f"Last {LENGTH - NUM_OF_LETTERS} characters must be digits.")

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
