from typing import List, Type, Generic

from sqlalchemy.orm import Session
from sqlalchemy_oso import roles as oso_roles
from .base import ModelType
from app.models import User


class RoleNameNotExistsError(Exception):
    """ Raised when role name does not exist """

    pass


class RoleBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        This class should be used when interacting with
        oso_roles. It helps to find out which roles are
        available for a specific resource and to add or
        remove roles for a specific user and resource
        """
        self.model = model

    def possible_roles(self) -> List[str]:
        resource_model = oso_roles.get_role_model_for_resource_model(self.model)
        return resource_model.choices

    def add_user_role(
        self, db: Session, user: User, resource: ModelType, role_name: str
    ):
        # verify that role_name is valid
        if role_name not in self.possible_roles():
            raise RoleNameNotExistsError

        oso_roles.add_user_role(db, user, resource, role_name)
        db.commit()

    def get_user_roles(
        self, db: Session, user: User, resource: ModelType
    ) -> List[ModelType]:
        return oso_roles.get_user_roles(db, user, self.model, resource_id=resource.id)

    def remove_user_role(
        self, db: Session, user: User, resource: ModelType, role_name: str
    ):
        oso_roles.delete_user_role(db, user, resource, role_name)
        db.commit()
