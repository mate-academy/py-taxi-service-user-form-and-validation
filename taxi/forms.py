from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from taxi.models import Driver, Car
from taxi.validators import validate_license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
        required=True
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class ToggleAssignToCarView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        current_user = request.user

        if current_user in car.drivers.all():
            car.drivers.remove(current_user)
        else:
            car.drivers.add(current_user)

        return redirect("taxi:car-detail", pk=pk)
