from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm


@login_required
def index(request):
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
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Create manufacturer"
        return super().get_context_data(**kwargs)


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Update manufacturer"
        return super().get_context_data(**kwargs)


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/class_confirm_delete.html"

    def get_context_data(self, **kwargs):
        kwargs["class_name"] = "manufacturer"
        return super().get_context_data(**kwargs)


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Create car"
        return super().get_context_data(**kwargs)


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Update car"
        return super().get_context_data(**kwargs)


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/class_confirm_delete.html"

    def get_context_data(self, **kwargs):
        kwargs["class_name"] = "car"
        return super().get_context_data(**kwargs)


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Create driver"
        return super().get_context_data(**kwargs)


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/class_form.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Update driver license"
        return super().get_context_data(**kwargs)


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/class_confirm_delete.html"

    def get_context_data(self, **kwargs):
        kwargs["class_name"] = "driver"
        return super().get_context_data(**kwargs)


class ToggleAssignToCarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        driver = Driver.objects.get(id=request.user.id)
        if (
                Car.objects.get(id=pk) in driver.cars.all()
        ):
            driver.cars.remove(pk)
        else:
            driver.cars.add(pk)
        return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
