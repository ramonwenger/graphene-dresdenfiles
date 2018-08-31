from django.db import models
from .spell import Spell

class Wizard(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    known_spells = models.ManyToManyField(Spell, related_name='known_by')
    __str__ = lambda self: self.name