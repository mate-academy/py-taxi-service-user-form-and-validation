from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    DriverCreateForm,
    DriverUpdateForm,
    DriverLicenseUpdateForm,
    CarForm)
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


@login_required
def assign_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "POST":
        if car.drivers.filter(pk=request.user.pk).exists():
            car.drivers.remove(request.user)
        else:
            car.drivers.add(request.user)

    return redirect("taxi:car-detail", pk=pk)


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
        context["is_driver_assigned"] = self.object.drivers.filter(
            pk=self.request.user.pk
        ).exists()
        return context


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
    paginate_by = 5

    def get_queryset(self):
        return get_user_model().objects.all()


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = DriverCreateForm
    success_url = reverse_lazy("taxi:driver-list")

    def get_queryset(self):
        return get_user_model().objects.all()


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = DriverUpdateForm
    success_url = reverse_lazy("taxi:driver-list")

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            data = self.request.POST.copy()
            driver = self.get_object()

            data.setdefault("username", driver.username)
            data.setdefault("first_name", driver.first_name)
            data.setdefault("last_name", driver.last_name)

            kwargs["data"] = data

        return kwargs


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")

    def get_queryset(self):
        return get_user_model().objects.all()


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy("taxi:driver-list")

    def get_queryset(self):
        return get_user_model().objects.all()


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    def get_queryset(self):
        return get_user_model().objects.prefetch_related("cars__manufacturer")
