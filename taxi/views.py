from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import DriverLicenseUpdateForm, DriverCreateForm, CarCreateForm
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
    success_url = reverse_lazy("taxi:car-list")
    form_class = CarCreateForm


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


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_form.html"
    form_class = DriverCreateForm


class DriverLicenseUpdateView(LoginRequiredMixin,
                              UserPassesTestMixin,
                              generic.UpdateView):
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/license_form.html"

    def get_success_url(self):
        return reverse_lazy("taxi:driver-detail",
                            kwargs={"pk": get_user(self.request).pk})

    def test_func(self):
        driver = self.get_object()
        return self.request.user.id == driver.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def handle_no_permission(self):
        return HttpResponseForbidden(
            "You are not allowed to update another driver's license number!"
        )


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


def driver_delete_from_car(request, driver_pk: int, car_pk: int):
    driver = get_object_or_404(Driver, pk=driver_pk)
    car = get_object_or_404(Car, pk=car_pk)
    car.drivers.remove(driver)
    return redirect("taxi:car-detail", pk=car.pk)


def driver_assign_to_car(request, driver_pk: int, car_pk: int):
    driver = get_object_or_404(Driver, pk=driver_pk)
    car = get_object_or_404(Car, pk=car_pk)
    car.drivers.add(driver)
    return redirect("taxi:car-detail", pk=car.pk)
