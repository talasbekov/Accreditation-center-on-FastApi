from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core import get_db

from services import attendee_service

router = APIRouter(
    prefix="/datas", tags=["Datas"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "/get_data_from_api",
    dependencies=[Depends(HTTPBearer())],
    response_model=dict,
    summary="Get all Cities"
)
async def get_data_from_kazintech(db: Session = Depends(get_db)):
    return await attendee_service.get_data_from_kazintech(db)
