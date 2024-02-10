from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverCreateForm, DriverLicenseUpdateForm, DriverDeleteForm, DriverUpdateForm
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
    fields = "__all__"
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
    template_name = "taxi/driver_detail.html"


class DriverCreateView(View):
    template_name = "taxi/create_driver.html"
    form_class = DriverCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taxi:driver-list')
        return render(request, self.template_name, {'form': form})


class DriverUpdateView(View):
    template_name = 'taxi/update_driver.html'
    form_class = DriverUpdateForm

    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        form = self.form_class(instance=driver)
        return render(request, self.template_name, {'driver': driver, 'form': form})

    def post(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        form = self.form_class(request.POST, instance=driver)

        if form.is_valid():
            form.save()
            return redirect('taxi:driver-list')

        return render(request, self.template_name, {'driver': driver, 'form': form})


class DriverLicenseUpdateView(View):
    template_name = 'taxi/update_license.html'
    form_class = DriverLicenseUpdateForm

    def get(self, request, driver_id):
        driver = get_object_or_404(Driver, pk=driver_id)
        form = self.form_class(instance=driver)
        return render(request, self.template_name, {'form': form, 'driver': driver})

    def post(self, request, driver_id):
        driver = get_object_or_404(Driver, pk=driver_id)
        form = self.form_class(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('taxi:driver-detail', driver_id=driver_id)
        return render(request, self.template_name, {'form': form, 'driver': driver})


class DriverDeleteView(View):
    template_name = 'taxi/delete_driver.html'

    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        return render(request, self.template_name, {'driver': driver})

    def post(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        form = DriverDeleteForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm_delete']:
            driver.delete()
            return redirect('taxi:driver-list')

        return render(request, self.template_name, {'driver': driver, 'form': form})