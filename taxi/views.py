from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django import forms

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


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    fields = [
        "username",
        "first_name",
        "last_name",
        "license_number",
        "password"
    ]
    success_url = reverse_lazy("taxi:driver-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_update_form.html"
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def add_driver_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.drivers.add(request.user)
    return redirect("taxi:car-detail", pk=pk)


@login_required
def remove_driver_from_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.drivers.remove(request.user)
    return redirect("taxi:car-detail", pk=pk)
