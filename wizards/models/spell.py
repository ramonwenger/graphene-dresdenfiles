from django.db import models


class Spell(models.Model):
    name = models.CharField(max_length=100)
    effect = models.TextField()
    __str__ = lambda self: self.name
