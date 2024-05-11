from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from taxi.forms import (CarForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm)
from taxi.models import Manufacturer, Car

User_model = get_user_model()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_cars = Car.objects.count()
    num_drivers = User_model.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {"num_cars": num_cars,
               "num_drivers": num_drivers,
               "num_manufacturers": num_manufacturers,
               "num_visits": request.session["num_visits"]}
    return render(request, template_name="taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all()
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = User_model
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = User_model
    queryset = User_model.objects.prefetch_related("cars__drivers")


class DriverCreateView(generic.CreateView):
    model = User_model
    form_class = DriverCreationForm


class DriverLisenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User_model
    form_class = DriverLicenseUpdateForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User_model
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/drivers_confirm_delete.html"


class CarsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_form.html"


class CarsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_form.html"


class CarsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_confirm_delete.html"


@login_required
def toggle_assign_to_car(request, pk) -> HttpResponseRedirect:
    if Car.objects.get(id=pk) in request.user.cars.all():
        request.user.cars.remove(pk)
    else:
        request.user.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


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
