from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverAssignForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        context["is_driver"] = self.request.user in car.drivers.all()
        return context


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    form_class = DriverAssignForm


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        context["car"] = car
        return context


class AssignDriverView(LoginRequiredMixin, View):
    model = Car
    template = "taxi/car_detail.html"

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)

        if request.user in car.drivers.all():
            car.drivers.remove(request.user)
        else:
            car.drivers.add(request.user)
        return redirect("taxi:car-detail", pk=car.pk)


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


class LicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    template_name = "taxi/license_form.html"
    form_class = DriverLicenseUpdateForm

    def get_success_url(self):
        driver = self.get_object()
        return reverse_lazy("taxi:driver-detail", kwargs={"pk": driver.pk})
