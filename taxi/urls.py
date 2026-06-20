from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    ToggleAssignToCarView,
    DriverListView,
    DriverDetailView,
    DriverCreateView,
    DriverLicenseUpdateView,
    DriverDeleteView,
    ManufacturerListView,
)

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),

    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),

    path(
        "cars/",
        CarListView.as_view(),
        name="car-list",
    ),
    path(
        "cars/create/",
        CarCreateView.as_view(),
        name="car-create",
    ),
    path(
        "cars/<int:pk>/",
        CarDetailView.as_view(),
        name="car-detail",
    ),
    path(
        "cars/<int:pk>/toggle-assign/",
        ToggleAssignToCarView.as_view(),
        name="car-toggle-assign",
    ),

    path(
        "drivers/",
        DriverListView.as_view(),
        name="driver-list",
    ),
    path(
        "drivers/create/",
        DriverCreateView.as_view(),
        name="driver-create",
    ),
    path(
        "drivers/<int:pk>/",
        DriverDetailView.as_view(),
        name="driver-detail",
    ),
    path(
        "drivers/<int:pk>/update/",
        DriverLicenseUpdateView.as_view(),
        name="driver-update",
    ),
    path(
        "drivers/<int:pk>/delete/",
        DriverDeleteView.as_view(),
        name="driver-delete",
    ),
]
