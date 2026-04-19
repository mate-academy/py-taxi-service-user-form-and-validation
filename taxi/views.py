from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
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
    User = get_user_model()
    model = User
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    User = get_user_model()
    model = User
    queryset = User.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    User = get_user_model()
    model = User
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    User = get_user_model()
    model = User
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "taxi:driver-detail",
            kwargs={"pk": self.object.pk}
        )


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    User = get_user_model()
    model = User
    success_url = reverse_lazy("taxi:driver-list")


def remove_driver_from_car(request, car_id, driver_id):
    if request.method == "POST":
        car = Car.objects.get(pk=car_id)
        user = get_user_model()
        driver = user.objects.get(pk=driver_id)
        car.drivers.remove(driver)

    return redirect("taxi:car-detail", pk=car_id)


def add_driver_to_car(request, car_id, driver_id):
    if request.method == "POST":
        car = Car.objects.get(pk=car_id)
        user = get_user_model()
        driver = user.objects.get(pk=driver_id)
        car.drivers.add(driver)

    return redirect("taxi:car-detail", pk=car_id)
