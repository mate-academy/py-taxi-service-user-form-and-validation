from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelMultipleChoiceField
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverRegisterForm, DriverLicenseUpdateForm, CarCreateForm
from .models import Driver, Car, Manufacturer


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car_drivers"] = self.object.drivers.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user in self.object.drivers.all():
            self.object.drivers.remove(request.user)
        else:
            self.object.drivers.add(request.user)
        return redirect(request.path)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreateForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_license_form"] = DriverLicenseUpdateForm()
        return context


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = DriverRegisterForm
    template_name = "taxi/driver_form.html"


def update_driver_license(request, pk):
    license_number = request.GET.get("license_number")
    license_number_form = DriverLicenseUpdateForm(
        {"license_number": license_number}
    )
    if license_number_form.is_valid():
        if not Driver.objects.filter(license_number=license_number):
            Driver.objects.filter(pk=pk).update(license_number=license_number)
        else:
            messages.error(
                request, f"driver license {license_number}"
                         f" is already in use"
            )
    else:
        messages.error(
            request,
            "Valid license number consists of 3 uppercase letters "
            "and 5 digits",
        )
    return redirect(request.META.get("HTTP_REFERER"))


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
