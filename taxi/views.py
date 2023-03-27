from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
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
    success_url = reverse_lazy("taxi:car-list")
    form_class = CarForm


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.object.pk})


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


def update_driver_license(request: HttpRequest, pk: int) -> HttpResponse:
    form = DriverLicenseUpdateForm()
    if request.method == "GET":
        return render(
            request, "taxi/update_driver_license.html", {"form": form}
        )

    if request.method == "POST":
        driver = get_object_or_404(Driver, pk=pk)
        form = DriverLicenseUpdateForm(request.POST)

        if form.is_valid():
            license_number = form.cleaned_data["license_number"]
            driver.license_number = license_number
            driver.save()
            return redirect("taxi:driver-detail", pk=pk)

    return render(request, "taxi/update_driver_license.html", {"form": form})


@login_required
def assign_driver_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    print("car")
    if request.method == "POST":
        print("post")
        car = get_object_or_404(Car, pk=car.pk)
        car.drivers.add(request.user.id)
        car.save()
        return redirect("taxi:car-detail", pk=car.pk)
    return render(request, "taxi/car_detail.html", {"car": car})


@login_required
def remove_driver_from_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car = get_object_or_404(Car, pk=car.pk)
        car.drivers.remove(request.user.id)
        car.save()
        return redirect("taxi:car-detail", pk=car.pk)
    return render(request, "taxi/car_detail.html", {"car": car})
