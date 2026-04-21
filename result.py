from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from routes.auth import get_current_user

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{student_id}")
def get_result(student_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    marks = db.query(models.Mark).filter(models.Mark.student_id == student_id).all()
    total_obtained = sum(m.internal_marks + m.external_marks for m in marks)
    
    total_max = 0
    for m in marks:
        subject = db.query(models.Subject).filter(models.Subject.id == m.subject_id).first()
        if subject:
            total_max += subject.max_internal + subject.max_external
    
    if total_max == 0:
        total_max = 100 * len(marks) # Default assumption
        
    percentage = (total_obtained / total_max * 100) if total_max > 0 else 0
    grade = 'F'
    if percentage >= 90:
        grade = 'A'
    elif percentage >= 80:
        grade = 'B'
    elif percentage >= 70:
        grade = 'C'
    elif percentage >= 60:
        grade = 'D'
    
    return {
        "student": student,
        "marks": marks,
        "total_obtained": total_obtained,
        "total_max": total_max,
        "percentage": percentage,
        "grade": grade
    }
