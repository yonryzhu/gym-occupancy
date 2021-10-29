from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends

import crud
import models
import schemas
from database import Session, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/records")
def get_all_records(
    db: Session = Depends(get_db),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list[schemas.Record]:
    records = crud.get_records(db, start_time, end_time)
    return records


@router.post("/records")
def create_record(
    record: schemas.Record, db: Session = Depends(get_db)
) -> schemas.Record:
    record = crud.create_record(db, record)
    return record


@router.patch("/records")
def create_records(records: list[schemas.Record], db: Session = Depends(get_db)):
    records = crud.create_records(db, records)
    return records
