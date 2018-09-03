from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
import graphene
from graphene import Node, relay, InputObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from .models import Wizard, Place, Spell


class WizardNode(DjangoObjectType):
    class Meta:
        model = Wizard
        interfaces = (Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'school': ['exact']
        }


class PlaceNode(DjangoObjectType):
    class Meta:
        model = Place
        interfaces = (Node,)
        filter_fields = ['name']


class SpellNode(DjangoObjectType):
    class Meta:
        model = Spell
        interfaces = (Node,)
        filter_fields = ['name']


class CreateWizardInput(InputObjectType):
    name = graphene.String(required=True)
    school = graphene.String(required=True)



class AddWizard(relay.ClientIDMutation):
    class Input:
        wizard = graphene.Argument(CreateWizardInput)

    new_wizard = graphene.Field(WizardNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        wizard_data = args.get('wizard')
        new_wizard = Wizard.objects.create(**wizard_data)
        return cls(new_wizard=new_wizard)


class UpdateWizard(relay.ClientIDMutation):
    class Input:
        wizard = graphene.Argument(CreateWizardInput)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    updated_wizard = graphene.Field(WizardNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        try:
            id = from_global_id(args.get('id'))[1]
            wizard = Wizard.objects.get(pk=id)
            if wizard:
                wizard_data = args.get('wizard')
                for key, value in wizard_data.items():
                    setattr(wizard, key, value)
                return cls(updated_wizard=wizard)
        except ValidationError as e:
            return cls(updated_wizard=None, errors=e)



class Mutation(graphene.ObjectType):
    add_wizard = AddWizard.Field()
    update_wizard = UpdateWizard.Field()


class Query(object):
    wizard = Node.Field(WizardNode)
    wizards = DjangoFilterConnectionField(WizardNode)
    places = DjangoFilterConnectionField(PlaceNode)
    spells = DjangoFilterConnectionField(SpellNode)

    # def resolve_wizard(self, info, *args, **kwargs):
    #     id = kwargs.get('id')
    #     name = kwargs.get('name')
    #
    #     if id is not None:
    #         return Wizard.objects.prefetch_related('known_spells').get(pk=id)
    #     if name is not None:
    #         return Wizard.objects.prefetch_related('known_spells').get(name=name)
    #
    #     return None

    def resolve_wizards(self, info, *args, **kwargs):
        return Wizard.objects.all()

    def resolve_places(self, info):
        return Place.objects.all()

    def resolve_spells(self, info):
        return Spell.objects.all()
