from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core import get_db
import logging
from services.record import data_service

# Настройка логирования
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/random/datas", tags=["Datass"], dependencies=[Depends(HTTPBearer())])

@router.post("/populate_all/", response_model=dict)
def populate_all(num_records: int, db: Session = Depends(get_db)):
    try:
        data_service.populate_all_tables(db, num_records)
        return {"status": f"Added {num_records} records to all tables"}
    except Exception as e:
        logger.error(f"Error populating tables: {e}")
        raise HTTPException(status_code=500, detail="Failed to populate tables due to a server error")
