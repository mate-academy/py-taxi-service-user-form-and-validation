from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Manufacturer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Driver
from .forms import DriverCreationForm
from django.contrib import messages
from .models import Car
from django.views.generic import UpdateView
from .forms import DriverLicenseUpdateForm
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import get_user_model
from .forms import CarCreateForm


Driver = get_user_model()

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


class CarCreateView(CreateView):
    model = Car
    form_class = CarCreateForm
    template_name = "taxi/car_form.html"
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


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")

    def form_valid(self, form):
        messages.success(self.request, "Driver created successfully!")
        return super().form_valid(form)


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.META.get(
            "HTTP_REFERER",
            reverse_lazy("taxi:driver-list")
        )
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Driver deleted successfully!")
        return super().delete(request, *args, **kwargs)


@login_required
def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        form = DriverLicenseUpdateForm(request.POST, instance=driver)
        print(f"Form is valid: {form.is_valid()}")
        if form.is_valid():
            print("Saving form and redirecting...")
            form.save()
            return redirect("taxi:driver-detail", pk=driver.pk)
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = DriverLicenseUpdateForm(instance=driver)
    return render(request, "taxi/update_license.html", {"form": form})

@login_required
def assign_me_to_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.drivers.add(request.user)
    messages.success(request, "You have been assigned to this car!")
    return redirect("car_detail", car_id=car.id)


@login_required
def remove_me_from_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.drivers.remove(request.user)
    messages.success(request, "You have been removed from this car!")
    return redirect("car_detail", car_id=car.id)


class DriverUpdateView(LoginRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")

    def form_valid(self, form):
        messages.success(self.request, "Driver updated successfully!")
        return super().form_valid(form)
