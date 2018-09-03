import graphene

import wizards.schema
from graphene_django.debug import DjangoDebug

from wizards.schema import Mutation


class Query(wizards.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
