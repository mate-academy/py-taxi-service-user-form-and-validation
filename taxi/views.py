from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarCreationForm
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

        if user.is_authenticated:
            context['is_driver'] = car.drivers.filter(id=user.id).exists()
        else:
            context['is_driver'] = False
        return context


class ToggleDriverView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        user = request.user

        if car.drivers.filter(id=user.id).exists():
            car.drivers.remove(user)
        else:
            car.drivers.add(user)

        return redirect('taxi:car-detail', pk=pk)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "taxi/car_form.html"
    form_class = CarCreationForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarCreationForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, CreateView):
    form_class = DriverCreationForm
    template_name = "taxi/driver_create_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateLicenseView(LoginRequiredMixin, UpdateView):
    template_name = "taxi/driver_license_update.html"
    form_class = DriverLicenseUpdateForm
    model = get_user_model()

    def get_success_url(self):
        return reverse_lazy("taxi:driver-detail", kwargs={"pk": self.object.pk})
