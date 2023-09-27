from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CompanyDetails(models.Model):
    company = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)

    def __str__(self):
        return self.company


class BikeList(models.Model):
    name = models.CharField(max_length=50)
    cc = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company_details = models.ForeignKey(
        CompanyDetails, on_delete=models.CASCADE, related_name="bikelist"
    )
    avg_rating = models.FloatField(default=0)
    number_of_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    bikelist = models.ForeignKey(
        BikeList, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return str(self.rating) + " | " + self.bikelist.name
