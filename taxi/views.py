from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import DriverLicenseUpdateForm, CarForm
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
        "num_visits": num_visits + 1
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
        driver_id = self.request.session.get("_auth_user_id")

        context["driver_id"] = driver_id
        context["is_driver_assigned"] = (
            int(driver_id) in list(
                self.object.drivers.values_list("id", flat=True)
            )
        )

        return context


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


class DriverCreateView(CreateView):
    model = Driver
    fields = ("license_number", "first_name", "last_name")

    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:index")


class DriverUpdateView(UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm


def delete_from_car(request: HttpRequest, car_id: int) -> HttpResponse:
    driver_id = request.session.get("_auth_user_id")
    car = Car.objects.get(pk=car_id)
    driver = Driver.objects.get(pk=driver_id)

    car.drivers.remove(driver)

    next_url = request.GET.get("next") or reverse("taxi:car-list")
    return HttpResponseRedirect(next_url)


def add_to_car(request: HttpRequest, car_id: int) -> HttpResponse:
    driver_id = request.session.get("_auth_user_id")
    car = Car.objects.get(pk=car_id)
    driver = Driver.objects.get(pk=driver_id)
    print(driver)

    car.drivers.add(driver)

    next_url = request.GET.get("next") or reverse("taxi:car-list")
    return HttpResponseRedirect(next_url)
