from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

from .models import Driver, Car, Manufacturer
from .forms import DriverLicenseUpdateForm, CarForm


@login_required
def index(request):
    """View function for the home page of the site."""
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        help_text="License number must be 3 uppercase letters followed by 5 digits (e.g., ABC12345)"
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'license_number')

    def clean_license_number(self):
        license_number = self.cleaned_data['license_number']

        if len(license_number) != 8:
            raise forms.ValidationError("License number must be exactly 8 characters long.")

        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise forms.ValidationError("First 3 characters must be uppercase letters.")

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits.")

        return license_number


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    template_name = 'taxi/driver_form.html'
    success_url = reverse_lazy('taxi:driver-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        return super().form_valid(form)


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = 'taxi/driver_confirm_delete.html'
    success_url = reverse_lazy('taxi:driver-list')


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = 'taxi/driver_license_update.html'
    success_url = reverse_lazy('taxi:driver-list')


@login_required
def assign_driver_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user not in car.drivers.all():
        car.drivers.add(request.user)
    return redirect('taxi:car-detail', pk=pk)


@login_required
def delete_driver_from_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user in car.drivers.all():
        car.drivers.remove(request.user)
    return redirect('taxi:car-detail', pk=pk)
