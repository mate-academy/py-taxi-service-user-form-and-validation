from django import forms
from .models import Car, Driver

class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Check the drivers to assign to this car."
    )

    class Meta:
        model = Car
        # list every field you want on the form; include 'drivers'
        fields = ['manufacturer', 'model', 'drivers']
