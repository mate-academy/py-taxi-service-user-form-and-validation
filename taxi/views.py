from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverLicenseUpdateForm, CarForm, DriverCreationForm
from .models import Car, Manufacturer

User = get_user_model()


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = User.objects.count()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        user = self.request.user

        is_driver = car.drivers.filter(pk=user.pk).exists()
        context["is_driver"] = is_driver

        return context


@login_required
def assign_driver_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user

    if not car.drivers.filter(pk=user.pk).exists():
        car.drivers.add(user)

    return redirect("taxi:car-detail", pk=pk)


@login_required
def delete_driver_from_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user
    if car.drivers.filter(pk=user.pk).exists():
        car.drivers.remove(user)

    return redirect("taxi:car-detail", pk=pk)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    # fields = "__all__"
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name = "driver"
    queryset = User.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def update_license_number(request, pk):
    driver = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = DriverLicenseUpdateForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Driver license number updated successfully.")
            return redirect("taxi:driver-detail", pk=driver.pk)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = DriverLicenseUpdateForm(instance=driver)

    return render(request, "taxi/driver_license_update.html",
                  {"form": form, "driver": driver})
