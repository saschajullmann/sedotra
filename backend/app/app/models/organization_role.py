from app.db.base_class import Base
from app.models import User, Organization
from sqlalchemy_oso.roles import resource_role_class

OrganizationRoleMixin = resource_role_class(
    Base, User, Organization, ["ADMIN", "LEAD", "MEMBER"]
)


class OrganizationRole(Base, OrganizationRoleMixin):
    pass
