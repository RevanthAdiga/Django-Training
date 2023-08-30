from django.db import models


class BikeList(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)

    def __str__(self):
        return self.name
