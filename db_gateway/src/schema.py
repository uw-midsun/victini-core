import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import RouteModel as RouteModelMeta
from database import db_session

from typing import Optional


class RouteModel(SQLAlchemyObjectType):
    class Meta:
        model = RouteModelMeta


class mutateRouteModel(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        lat = graphene.Float()
        lon = graphene.Float()

    ok = graphene.Boolean()
    routemodel = graphene.Field(RouteModel)

    def mutate(
        root, info, id, lat: Optional[float] = None, lon: Optional[float] = None
    ):
        routemodel = db_session.query(RouteModelMeta).filter_by(id=id).first()
        if lat:
            routemodel.lat = lat
        if lon:
            routemodel.lon = lon
        db_session.commit()
        return mutateRouteModel(ok=True, routemodel=routemodel)


class Mutation(graphene.ObjectType):
    mutate_routemodel = mutateRouteModel.Field()


class Query(graphene.ObjectType):
    query_routemodel = graphene.Field(RouteModel, id=graphene.Int())

    def resolve_query_routemodel(root, info, id):
        return db_session.query(RouteModelMeta).filter_by(id=id).first()


schema = graphene.Schema(query=Query, mutation=Mutation)
