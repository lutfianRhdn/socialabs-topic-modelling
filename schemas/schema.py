import strawberry
from schemas.queries import Query

schema = strawberry.federation.Schema(
    query=Query,
    enable_federation_2=True
)