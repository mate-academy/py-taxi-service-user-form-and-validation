from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    DriverCreationForm,
    CarCreationForm,
    DriverLicenseUpdateForm
)

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


class ManufacturerBaseView(LoginRequiredMixin, generic.View):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    fields = "__all__"


class ManufacturerListView(ManufacturerBaseView, generic.ListView):
    paginate_by = 5


class ManufacturerCreateView(ManufacturerBaseView, generic.CreateView):
    pass


class ManufacturerUpdateView(ManufacturerBaseView, generic.UpdateView):
    pass


class ManufacturerDeleteView(ManufacturerBaseView, generic.DeleteView):
    pass


class CarBaseView(LoginRequiredMixin, generic.View):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class CarListView(CarBaseView, generic.ListView):
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(CarBaseView, generic.DetailView):
    pass


class CarCreateView(CarBaseView, generic.CreateView):
    form_class = CarCreationForm


class CarUpdateView(CarBaseView, generic.UpdateView):
    fields = "__all__"


class CarDeleteView(CarBaseView, generic.DeleteView):
    pass


class DriverBaseView(LoginRequiredMixin, generic.View):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")


class DriverListView(DriverBaseView, generic.ListView):
    paginate_by = 5


class DriverDetailView(DriverBaseView, generic.DetailView):
    queryset = DriverBaseView.model.objects.all().prefetch_related(
        "cars__manufacturer")


class DriverCreateView(DriverBaseView, generic.CreateView):
    form_class = DriverCreationForm


class DriverDeleteView(DriverBaseView, generic.DeleteView):
    pass


class DriverUpdateView(DriverBaseView, generic.UpdateView):
    form_class = DriverLicenseUpdateForm


@login_required
def assign_or_remove_driver_from_car(request, pk):
    if request.method == "POST":
        driver = request.user
        car = get_object_or_404(Car, pk=pk)

        # Ensure the current driver is assigned to the car
        if driver in car.drivers.all():
            car.drivers.remove(driver)
        else:
            car.drivers.add(driver)

        return HttpResponseRedirect(
            reverse_lazy("taxi:car-detail", kwargs={"pk": car.id})
        )

    return HttpResponse("Method Not Allowed", status=405)
