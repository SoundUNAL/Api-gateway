from fastapi import APIRouter
import strawberry
from strawberry.asgi import GraphQL
from strawberry.tools import merge_types
from schemas.audio_manegement.index import queries as audio_manegement_queries, mutations as audio_manegement_mutations
# from schemas.users.index import queries as users_queries, mutations as users_mutations
from schemas.interactions.index import queries as interactions_queries, mutations as interactions_mutations
from schemas.notification_management.index import queries as notification_queries, mutations as notification_mutations

app_graphql = APIRouter()

# All queries

queries = audio_manegement_queries + interactions_queries + notification_queries
mutations = audio_manegement_mutations + \
    interactions_mutations + notification_mutations

# Merge schemas

Query = merge_types("Query", queries)
Mutation = merge_types("Mutation", mutations)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)


app_graphql.add_route('/graphql', graphql_app)

# :v Tatiana was here