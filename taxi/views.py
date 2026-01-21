from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView

from taxi.forms import (
    DriverCreateForm,
    DriverLicenseUpdateForm,
    DriverUpdateForm,
)
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


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"
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
    template_name = "taxi/driver_detail.html"


class DriverCreateView(FormView):
    template_name = "taxi/create_driver.html"
    form_class = DriverCreateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(UpdateView):
    model = Driver
    form_class = DriverUpdateForm
    template_name = "taxi/update_driver.html"
    success_url = reverse_lazy("taxi:driver-list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Driver, pk=pk)


class DriverLicenseUpdateView(View):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/update_license.html"

    def form_valid(self, form):
        driver = form.save()
        return redirect("taxi:driver-detail", driver_id=driver.id)

    def get_object(self, queryset=None):
        driver_id = self.kwargs.get("driver_id")
        return get_object_or_404(Driver, pk=driver_id)


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "taxi/delete_driver.html"
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
