# taxi/urls.py
from django.urls import path
from .views import (
    # ... other views
    DriverCreateView,
    DriverDeleteView,
    DriverLicenseUpdateView,
    toggle_assign_to_car,
)

urlpatterns = [
    # ... existing patterns
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
    path("drivers/<int:pk>/update-license/", DriverLicenseUpdateView.as_view(), name="driver-update-license"),
    path("cars/<int:pk>/toggle-assign/", toggle_assign_to_car, name="toggle-car-assign"),
]
