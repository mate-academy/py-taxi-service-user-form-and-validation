from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.http import require_POST

from .models import Car, Manufacturer
from .forms import DriverLicenseUpdateForm, DriverCreationForm, CarForm

User = get_user_model()


@login_required
def index(request):
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
    return render(request, "taxi/index.html", context)


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class ManufacturerCreateView(generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(generic.DetailView):
    model = Car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        request = self.request
        context["is_driver"] = car.drivers.filter(pk=request.user.pk).exists()
        return context


class CarCreateView(generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


@require_POST
@login_required
def assign_me_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.drivers.add(request.user)
    return redirect("taxi:car-detail", pk=pk)


@require_POST
@login_required
def delete_me_from_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.drivers.remove(request.user)
    return redirect("taxi:car-detail", pk=pk)


class DriverListView(generic.ListView):
    model = User
    paginate_by = 5


class DriverDetailView(generic.DetailView):
    model = User
    queryset = User.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(generic.CreateView):
    model = User
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(generic.DeleteView):
    model = User
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(generic.UpdateView):
    model = User
    form_class = DriverLicenseUpdateForm

    def get_success_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.object.pk})
