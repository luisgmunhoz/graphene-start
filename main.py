from typing import Any, Optional
import typing
from graphene import Field, List, Schema, ObjectType, String, Int


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())
    # dummy data store
    users = [
        {"id": 1, "name": "John", "age": 20},
        {"id": 2, "name": "Jane", "age": 22},
        {"id": 3, "name": "Bob", "age": 30},
        {"id": 4, "name": "Alice", "age": 25},
    ]

    @staticmethod
    def resolve_user(root: Optional[Any], info: Any, user_id: int) -> Optional[Field]:
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(
        root: Optional[Any], info: Any, min_age: int
    ) -> typing.List[Field]:
        return [user for user in Query.users if user["age"] >= min_age]


schema = Schema(query=Query)

# gql = """
# query {
#     user(user_id: 4){
#         id
#         name
#         age
#     }
# }
# """

gql = """
query {
    usersByMinAge(minAge: 25){
        id
        name
        age
    }
}
"""

if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
