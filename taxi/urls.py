from django.urls import path
from . import views

app_name = "taxi"

urlpatterns = [
    # Página inicial opcional
    path("", views.HomeView.as_view(), name="home"),

    # Motoristas
    path("drivers/", views.DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", views.DriverDetailView.as_view(), name="driver-detail"),
    path("drivers/create/", views.DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/delete/", views.DriverDeleteView.as_view(), name="driver-delete"),
    path("drivers/<int:pk>/update-license/", views.DriverLicenseUpdateView.as_view(), name="driver-update-license"),

    # Carros
    path("cars/", views.CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", views.CarDetailView.as_view(), name="car-detail"),
    path("cars/<int:pk>/update/", views.CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/assign/", views.assign_driver_to_car, name="car-assign"),
    path("cars/<int:pk>/remove/", views.remove_driver_from_car, name="car-remove"),
]
