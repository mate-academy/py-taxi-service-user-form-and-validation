from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Car, Manufacturer


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


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def assign_me_to_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    car.drivers.add(request.user)
    return redirect("taxi:car-detail", pk=pk)


@login_required
def delete_me_from_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    car.drivers.remove(request.user)
    return redirect("taxi:car-detail", pk=pk)
