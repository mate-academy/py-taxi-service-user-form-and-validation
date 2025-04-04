from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    ManufacturerForm,
)
from .models import Driver, Car, Manufacturer


@login_required
def index(request):

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
    context_object_name = "manufacturers"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = False
        return context


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    template_name = "taxi/manufacturer_confirm_delete.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = "taxi/car_list.html"
    context_object_name = "cars"
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"
    queryset = Car.objects.all().prefetch_related("drivers")


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = False
        return context


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    template_name = "taxi/car_confirm_delete.html"
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    template_name = "taxi/driver_list.html"
    context_object_name = "driver_list"
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_update_form.html"
    success_url = reverse_lazy("taxi:driver-list")

    def get_object(self, queryset=None):
        return self.request.user


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    car = Car.objects.get(id=pk)
    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)
    return HttpResponseRedirect(reverse("taxi:car-detail",
                                        args=[pk]))
