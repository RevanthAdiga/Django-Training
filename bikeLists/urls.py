from django.urls import path

from . import views

urlpatterns = [
    path("", views.BikeListAV.as_view(), name="bike list"),
    path("<int:pk>", views.BikeDetailAV.as_view(), name="bike detail"),
]
