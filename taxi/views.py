from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("taxi:driver-list")
        )
        return context


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car

    def post(self, request, *args, **kwargs):
        car = self.get_object()

        if "assign" in request.POST:
            car.drivers.add(request.user)
        elif "remove" in request.POST:
            car.drivers.remove(request.user)

        return redirect("taxi:car-detail", pk=car.pk)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("taxi:driver-list")
        )
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("taxi:driver-list")
        )
        return context


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    context_object_name = "driver"
    success_url = reverse_lazy("taxi:driver-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("taxi:driver-list")
        )
        return context


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("taxi:driver-list")
        )
        return context
