from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views import generic

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
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


class CancelUrlMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer = self.request.META.get("HTTP_REFERER", "")
        if referer and url_has_allowed_host_and_scheme(
            referer,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            context["cancel_url"] = referer
        else:
            context["cancel_url"] = self.get_fallback_cancel_url()
        return context

    def get_fallback_cancel_url(self):
        return reverse_lazy("taxi:index")


class ManufacturerDeleteView(
    CancelUrlMixin,
    LoginRequiredMixin,
    generic.DeleteView,
):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = Car.objects.select_related("manufacturer").prefetch_related(
        "drivers"
    )


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(CancelUrlMixin, LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")

    def get_fallback_cancel_url(self):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.object.pk})


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    context_object_name = "driver"
    queryset = get_user_model().objects.all().prefetch_related(
        "cars__manufacturer"
    )


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_form.html"
    context_object_name = "driver"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(CancelUrlMixin, LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    context_object_name = "driver"
    success_url = reverse_lazy("taxi:driver-list")

    def get_fallback_cancel_url(self):
        return reverse_lazy(
            "taxi:driver-detail",
            kwargs={"pk": self.object.pk},
        )


class CarDriverAssignmentView(LoginRequiredMixin, View):
    action = None

    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=kwargs["pk"])
        getattr(car.drivers, self.action)(request.user)
        return redirect("taxi:car-detail", pk=car.pk)


class CarAssignMeView(CarDriverAssignmentView):
    action = "add"


class CarRemoveMeView(CarDriverAssignmentView):
    action = "remove"
