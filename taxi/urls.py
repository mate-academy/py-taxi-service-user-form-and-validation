from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverCreateView,
    DriverDeleteView,
    DriverDetailView,
    DriverLicenseUpdateView,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    CarDriverUpdateView,
    add_driver_to_car,
    delete_driver_from_car,
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
    path(
        "cars/<int:pk>/car-driver-update/",
        CarDriverUpdateView.as_view(),
        name="car-driver-update"
    ),
    path(
        "cars/<int:pk>/add-driver-to-car/",
        add_driver_to_car,
        name="add-driver-to-car"
    ),
    path(
        "cars/<int:pk>/delete-driver-from-car/",
        delete_driver_from_car,
        name="delete-driver-from-car"
    ),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path(
        "drivers/create/", DriverCreateView.as_view(), name="driver-create"
    ),
    path(
        "drivers/<int:pk>/delete/",
        DriverDeleteView.as_view(),
        name="driver-delete"
    ),
    path(
        "drivers/<int:pk>/license-update/",
        DriverLicenseUpdateView.as_view(),
        name="driver-update"
    ),
]

app_name = "taxi"
