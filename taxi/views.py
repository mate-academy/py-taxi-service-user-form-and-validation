from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from .forms import DriverLicenseUpdateForm, CarCreateForm
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


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
    success_url = reverse_lazy("taxi:driver-list")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    fields = "__all__"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(generic.UpdateView):
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_update.html"

    def get_object(self, queryset=None):
        return Driver.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy(
            "taxi:driver-detail", kwargs={"pk": self.object.pk}
        )


class CarAssignDriverView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("taxi:car-list")

    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=self.kwargs["pk"])
        if request.user in car.drivers.all():
            car.drivers.remove(request.user)
            messages.success(
                request, f"You have been removed from the car {car}"
            )
        else:
            car.drivers.add(request.user)
            messages.success(
                request, f"You have been assigned to the car {car}"
            )
        return super().post(request, *args, **kwargs)
