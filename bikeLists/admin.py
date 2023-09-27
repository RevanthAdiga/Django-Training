from django.contrib import admin

# Register your models here.
from .models import BikeList, CompanyDetails, Review

admin.site.register([BikeList, CompanyDetails, Review])
