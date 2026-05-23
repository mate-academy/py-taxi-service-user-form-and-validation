from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from .models import Car, Manufacturer


@login_required
def index(request):
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


class ManufacturerListView(LoginRequiredMixin, ListView):
    model = Manufacturer
    paginate_by = 5


class ManufacturerCreateView(LoginRequiredMixin, CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class ToggleAssignCarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        driver = request.user

        if car in driver.cars.all():
            driver.cars.remove(car)
        else:
            driver.cars.add(car)

        return HttpResponseRedirect(
            reverse_lazy("taxi:car-detail", kwargs={"pk": pk})
        )


class DriverListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    queryset = (
        get_user_model().objects.all()
        .prefetch_related("cars__manufacturer")
    )


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")

    def get_success_url(self):
        return reverse_lazy(
            "taxi:driver-detail",
            kwargs={"pk": self.object.pk},
        )


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")
