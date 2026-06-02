from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from .models import Driver, Car, Manufacturer
from django.views.generic import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy


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


# --- MANUFACTURER VIEWS ---

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


# --- CAR VIEWS ---

class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


# --- DRIVER VIEWS ---

class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(LoginRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm  # ось тут
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")


# In taxi/views.py
class DriverLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_form.html"

    def get_success_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@login_required
def toggle_assign_to_car(request, pk):
    """Assign or remove the logged-in driver from a specific car."""
    car = get_object_or_404(Car, pk=pk)
    driver = request.user

    if driver in car.drivers.all():
        car.drivers.remove(driver)
    else:
        car.drivers.add(driver)

    return HttpResponseRedirect(reverse("taxi:car-detail", kwargs={"pk": pk}))
