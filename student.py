from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from routes.auth import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    from routes.auth import get_password_hash
    
    db_student = db.query(models.Student).filter(models.Student.roll_number == student.roll_number).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    db_user = db.query(models.User).filter(models.User.username == student.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered as a login user")
        
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    
    new_user = models.User(
        username=student.email,
        hashed_password=get_password_hash(student.roll_number),
        role='student'
    )
    db.add(new_user)
    
    db.commit()
    db.refresh(new_student)
    return new_student

