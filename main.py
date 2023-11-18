from typing import Any, List, Optional
from graphene import (
    Field,
    List as GrapheneList,
    Schema,
    ObjectType,
    String,
    Int,
    Mutation as GrapheneMutation,
)


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(GrapheneMutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root: Optional[Any], info: Any, name: str, age: int) -> "CreateUser":
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


class UpdateUser(GrapheneMutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(
        root: Optional[Any],
        info: Any,
        user_id: int,
        name: Optional[str] = None,
        age: Optional[int] = None,
    ) -> Optional["UpdateUser"]:
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        if not user:
            return None

        if name:
            user["name"] = name
        if age:
            user["age"] = age
        return UpdateUser(user=user)


class DeleteUser(GrapheneMutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root: Optional[Any], info: Any, user_id: int) -> Optional["DeleteUser"]:
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        if not user:
            return None

        Query.users.remove(user)
        return DeleteUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = GrapheneList(UserType, min_age=Int())
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
    ) -> List[Field]:
        return [
            user
            for user in Query.users
            if isinstance(user["age"], int) and user["age"] >= min_age
        ]


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

gql_query = """
query {
    user(userId: 1){
        id
        name
        age
    }
}
"""

gql_create = """
mutation {
    createUser(name: "test", age: 20){
        user {
            id
            name
            age
        }
    }
}
"""

gql_update = """
mutation {
    updateUser(userId: 1, name: "test", age: 20){
        user {
            id
            name
            age
        }
    }
}
"""

gql_delete = """
mutation {
    deleteUser(userId: 1){
        user {
            id
            name
            age
        }
    }
}
"""


gql_query_min_age = """
query {
    usersByMinAge(minAge: 25){
        id
        name
        age
    }
}
"""

if __name__ == "__main__":
    result = schema.execute(gql_create)
    print(result)
    result2 = schema.execute(gql_query)
    print(result2)
    result3 = schema.execute(gql_update)
    print(result3)
    result4 = schema.execute(gql_query)
    print(result4)
    result5 = schema.execute(gql_delete)
    print(result5)
    result6 = schema.execute(gql_query)
    print(result6)
    result7 = schema.execute(gql_query_min_age)
    print(result7)
