from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=100)
    __str__ = lambda self: self.name
