from datetime import timedelta
from typing import Dict
from app.core.security import create_access_token
from app.models import User


def create_access_header(user: User) -> Dict[str, str]:
    access_token = create_access_token(user.id, expires_delta=timedelta(minutes=5))
    return {"Authorization": f"Bearer {access_token}"}
