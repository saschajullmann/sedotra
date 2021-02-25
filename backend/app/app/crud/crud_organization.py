from app.crud.base import CRUDBase
from app.models import Organization
from app.schemas import OrgCreate, OrgUpdate


class CRUDOrg(CRUDBase[Organization, OrgCreate, OrgUpdate]):
    pass


org = CRUDOrg(Organization)
