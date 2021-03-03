from typing import Optional
from pydantic import BaseModel


class OrgBase(BaseModel):
    name: str
    description: Optional[str] = None


class OrgCreate(OrgBase):
    pass


class OrgUpdate(OrgBase):
    pass
