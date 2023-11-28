from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CarForm, DriverLicenseUpdateForm, DriverCreationForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_drivers = get_user_model().objects.count()
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


@login_required()
def car_driver_assignment(
        request: HttpRequest,
        pk: int,
        driver_id: int
) -> HttpResponse:
    car = Car.objects.get(pk=pk)
    driver = get_user_model().objects.get(pk=driver_id)

    if driver in car.drivers.all():
        car.drivers.remove(driver_id)
    else:
        car.drivers.add(driver_id)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


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
    form_class = CarForm


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    form_class = CarForm


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = (get_user_model().objects
                .prefetch_related("cars__manufacturer"))


class DriverCreateView(generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm


class DriverUpdateView(generic.UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm


class DriverDeleteView(generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirmation_delete.html"
