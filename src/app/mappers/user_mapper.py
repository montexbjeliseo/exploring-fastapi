from app.models.users import User
from app.schemas.user_schemas import UserModel


def to_user_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role.name
    )


def to_user_model_list(users):
    return [to_user_model(user) for user in users]
