import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import RouteModel as RouteModelMeta, Weather as WeatherMeta
from database import db_session

from typing import Optional


class RouteModel(SQLAlchemyObjectType):
    class Meta:
        model = RouteModelMeta
        
class Weather(SQLAlchemyObjectType):
    class Meta:
        model = WeatherMeta

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

class mutateWeatherModel(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        lat = graphene.Float()
        lon = graphene.Float()
        temperature = graphene.Float()
        humidity = graphene.Float()
        wind_speed = graphene.Float()
        wind_direction = graphene.Float()
        cloud_cover = graphene.Float()
    
    ok = graphene.Boolean()
    weather = graphene.Field(Weather)

    def mutate(
        root, info, id, lat: Optional[float] = None, lon: Optional[float] = None,
        temperature: Optional[float] = None, humidity: Optional[float] = None,
        wind_speed: Optional[float] = None, wind_direction: Optional[float] = None,
        cloud_cover: Optional[float] = None
    ):
        weather = db_session.query(WeatherMeta).filter_by(id=id).first()
        if lat:
            weather.lat = lat
        if lon:
            weather.lon = lon
        if temperature:
            weather.temperature = temperature
        if humidity:
            weather.humidity = humidity
        if wind_speed:
            weather.wind_speed = wind_speed
        if wind_direction:
            weather.wind_direction = wind_direction
        if cloud_cover:
            weather.cloud_cover = cloud_cover
        db_session.commit()
        return mutateWeatherModel(ok=True, weather=weather)

class Mutation(graphene.ObjectType):
    mutate_routemodel = mutateRouteModel.Field()
    mutate_weather = mutateWeatherModel.Field()

class Query(graphene.ObjectType):
    query_routemodel = graphene.Field(RouteModel, id=graphene.Int())
    query_weather = graphene.Field(Weather, id=graphene.Int())

    def resolve_query_routemodel(root, info, id):
        return db_session.query(RouteModelMeta).filter_by(id=id).first()

    def resolve_query_weather(root, info, id):
        return db_session.query(WeatherMeta).filter_by(id=id).first()

schema = graphene.Schema(query=Query, mutation=Mutation)
