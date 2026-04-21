from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from routes.auth import get_current_user

router = APIRouter(prefix="/marks", tags=["marks"])

@router.post("/", response_model=schemas.MarkResponse)
def create_mark(mark: schemas.MarkCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_mark = models.Mark(**mark.model_dump())
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark
