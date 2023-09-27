from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("company/", views.Company, basename="company")
urlpatterns = [
    path("bikes/", views.BikeListAV.as_view(), name="bikelist"),
    path("bikes/<int:pk>/", views.BikeDetailAV.as_view(), name="bikedetail"),
    path("", include(router.urls)),
    # path("company", views.CompanyAv.as_view(), name="company"),
    # path("company/<int:pk>", views.CompanyDetailAV.as_view(), name="companydetail"),
    path("<int:pk>/review/", views.ReviewList.as_view(), name="reviews"),
    path("<int:pk>/review-create/", views.ReviewCreate.as_view(), name="review-create"),
    path("review/<int:pk>/", views.ReviewDetail.as_view(), name="review"),
]
