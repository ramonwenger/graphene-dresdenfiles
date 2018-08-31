from graphene_django import DjangoObjectType
import graphene

from .models import Wizard, Place, Spell


class WizardType(DjangoObjectType):
    class Meta:
        model = Wizard


class PlaceType(DjangoObjectType):
    class Meta:
        model = Place


class SpellType(DjangoObjectType):
    class Meta:
        model = Spell

class Query(object):
    wizard = graphene.Field(WizardType, id=graphene.Int(), name=graphene.String())
    wizards = graphene.List(WizardType)
    places = graphene.List(PlaceType)
    spells = graphene.List(SpellType)

    def resolve_wizard(self, info, *args, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Wizard.objects.prefetch_related('known_spells').get(pk=id)
        if name is not None:
            return Wizard.objects.prefetch_related('known_spells').get(name=name)

        return None

    def resolve_wizards(self, info):
        return Wizard.objects.all()

    def resolve_places(self, info):
        return Place.objects.all()

    def resolve_spells(self, info):
        return Spell.objects.all()