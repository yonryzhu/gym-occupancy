from datetime import datetime
from typing import Optional

import models
import schemas
from database import Session


def get_records(
    db: Session,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list[models.Record]:
    q = db.query(models.Record)
    if start_time is not None:
        q = q.filter(models.Record.timestamp > start_time)
    if end_time is not None:
        q = q.filter(models.Record.timestamp < end_time)
    return q.all()


def create_record(db: Session, record: schemas.Record):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def create_records(db: Session, records: list[schemas.Record]):
    db_records = []
    for record in records:
        db_record = models.Record(**record.dict())
        db_records.append(db_record)
    db.add_all(db_records)
    db.commit()
    for db_record in db_records:
        db.refresh(db_record)
    return db_records
