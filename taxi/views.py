from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Car, Driver, Manufacturer


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "taxi/index.html"


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


def assign_me_to_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    car.drivers.add(request.user)
    return redirect("taxi:car-detail", pk=pk)


def delete_me_from_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    car.drivers.remove(request.user)
    return redirect("taxi:car-detail", pk=pk)
