from django.contrib import admin

# Register your models here.
from .models import Bike, CompanyDetails, Review

admin.site.register([Bike, CompanyDetails, Review])
