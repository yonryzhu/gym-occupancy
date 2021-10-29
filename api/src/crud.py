import models
import schemas
from database import Session


def get_records(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Record).offset(offset).limit(limit).all()


def create_record(db: Session, record: schemas.Record):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
