from django.urls import path, include

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
    LicenseNumberUpdateView,
    assign_delete_to_car,
)

cars_patterns = [
    path("", CarListView.as_view(), name="car-list"),
    path("create/", CarCreateView.as_view(), name="car-create"),
    path(
        "<int:pk>/",
        include(
            [
                path("", CarDetailView.as_view(), name="car-detail"),
                path("update/", CarUpdateView.as_view(), name="car-update"),
                path("delete/", CarDeleteView.as_view(), name="car-delete"),
                path(
                    "delete-assign/",
                    assign_delete_to_car,
                    name="unassign-car-assign",
                ),
            ]
        ),
    ),
]

manufacturers_patterns = [
    path(
        "",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "<int:pk>/",
        include(
            [
                path(
                    "update/",
                    ManufacturerUpdateView.as_view(),
                    name="manufacturer-update",
                ),
                path(
                    "delete/",
                    ManufacturerDeleteView.as_view(),
                    name="manufacturer-delete",
                ),
            ]
        ),
    ),
]

drivers_patterns = [
    path("", DriverListView.as_view(), name="driver-list"),
    path("create/", DriverCreateView.as_view(), name="driver-create"),
    path(
        "<int:pk>/",
        include(
            [
                path("", DriverDetailView.as_view(), name="driver-detail"),
                path(
                    "update/",
                    LicenseNumberUpdateView.as_view(),
                    name="driver-update",
                ),
                path(
                    "delete/", DriverDeleteView.as_view(), name="driver-delete"
                ),
                path(
                    "license-update/",
                    LicenseNumberUpdateView.as_view(),
                    name="driver-licence-update",
                ),
            ]
        ),
    ),
]

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", include(manufacturers_patterns)),
    path("cars/", include(cars_patterns)),
    path("drivers/", include(drivers_patterns)),
]

app_name = "taxi"
