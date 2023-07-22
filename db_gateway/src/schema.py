import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import RouteModel as RouteModelMeta


class RouteModel(SQLAlchemyObjectType):
    class Meta:
        model = RouteModelMeta
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allow only single column sorting
    # all_employees = SQLAlchemyConnectionField(
    #     Employee.connection, sort=Employee.sort_argument()
    # )
    # # Allows sorting over multiple columns, by default over the primary key
    # all_roles = SQLAlchemyConnectionField(Role.connection)
    # # Disable sorting over this field
    # all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)
    all_routemodel = SQLAlchemyConnectionField(
        RouteModel.connection, sort=RouteModel.sort_argument()
    )


schema = graphene.Schema(query=Query)
