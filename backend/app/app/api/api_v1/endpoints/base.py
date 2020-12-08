from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck")
def healthcheck() -> Any:
    """
    Healthcheck endpoint
    """
    return "OK"
