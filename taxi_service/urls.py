from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("taxi:driver-list")),  # Redireciona a raiz para a lista de motoristas
    path("accounts/", include("django.contrib.auth.urls")),  # Login, logout, etc.
    path("__debug__/", include("debug_toolbar.urls")),       # Debug toolbar
    path("", include("taxi.urls", namespace="taxi")),         # URLs do app taxi
]
