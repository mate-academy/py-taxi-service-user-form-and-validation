from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    DriverCreateView,
    DriverDeleteView,
    DriverLicenseUpdateView,
    LicenseNumberDeleteView,
    car_add_driver,
    car_delete_driver,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path(
        "driver/create/",
        DriverCreateView.as_view(),
        name="driver-create",
    ),
    path("driver/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
    path("license_number/<int:pk>/delete/", LicenseNumberDeleteView.as_view(), name="license_number-delete"),
    path("driver/<int:pk>/update/", DriverLicenseUpdateView.as_view(), name="driver-update"),
    path("cars/<int:pk>/add-driver/", car_add_driver, name="add-driver"),
    path("cars/<int:pk>/delete-driver/", car_delete_driver, name="delete-driver"),
]

app_name = "taxi"
