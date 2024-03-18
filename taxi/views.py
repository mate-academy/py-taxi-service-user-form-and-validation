from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer

from taxi.forms import (
    DriverLicenseUpdateForm,
    CustomDriverCreateForm,
    CarCreateForm
)


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


@login_required()
def car_detail(request, pk: int) -> HttpResponse:
    car = Car.objects.get(pk=pk)
    context = {
        "car": car
    }
    if request.method == "GET":
        return render(request, "taxi/car_detail.html", context=context)

    if request.method == "POST":
        driver = get_user_model().objects.get(pk=request.user.pk)
        if "assign" in request.POST:
            car.drivers.add(driver)
        if "remove" in request.POST:
            car.drivers.remove(driver)

    return render(request, "taxi/car_detail.html", context=context)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreateForm
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


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = CustomDriverCreateForm


class DriverUpdateLicenseNumberView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class CarDriverAction(LoginRequiredMixin, generic.FormView):
    def form_valid(self, form):
        car_id = self.kwargs["pk"]
        car = Car.objects.get(pk=car_id)
        driver = Driver.objects.get(pk=self.request.user.pk)

        if "assign" in self.request.POST:
            car.drivers.add(driver)
        if "remove" in self.request.POST:
            car.drivers.remove(driver)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("taxi:car-list")
