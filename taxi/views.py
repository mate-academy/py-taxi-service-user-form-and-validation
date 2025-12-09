from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer

from .forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm

UserModel = get_user_model()


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = UserModel.objects.count()
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
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = UserModel
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserModel
    queryset = UserModel.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserModel
    form_class = DriverCreationForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserModel
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdate(LoginRequiredMixin, generic.UpdateView):
    model = UserModel
    form_class = DriverLicenseUpdateForm


@login_required
def assign_me_to_car(request, pk):
    if request.method == "POST":
        user = request.user.id
        car = Car.objects.get(id=pk)
        driver = UserModel.objects.get(id=user)
        car.drivers.add(driver)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_driver_from_car(request, pk):
    if request.method == "POST":
        user = request.user.id
        car = Car.objects.get(id=pk)
        driver = UserModel.objects.get(id=user)
        car.drivers.remove(driver)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
