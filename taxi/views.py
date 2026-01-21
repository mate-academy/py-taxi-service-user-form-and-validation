from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarCreationForm


User = get_user_model()


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


# Manufacturer
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


# Cars
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


class ToggleCarDriverView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        driver = request.user
        if driver in car.drivers.all():
            car.drivers.remove(driver)
        else:
            car.drivers.add(driver)
        return redirect("taxi:car-detail", pk=pk)


# Drivers
class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    context_object_name = "driver_list"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
    context_object_name = "driver"


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = DriverLicenseUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "taxi:driver-detail",
            kwargs={"pk": self.object.pk}
        )


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("taxi:driver-list")
