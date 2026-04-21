import database
import models
from routes.auth import get_password_hash

Base = database.Base
engine = database.engine
Base.metadata.create_all(bind=engine)

db = database.SessionLocal()

admin_user = db.query(models.User).filter(models.User.username == 'admin').first()
if not admin_user:
    admin_user = models.User(username='admin', hashed_password=get_password_hash('admin'), role='admin')
    db.add(admin_user)

teacher_user = db.query(models.User).filter(models.User.username == 'teacher').first()
if not teacher_user:
    teacher_user = models.User(username='teacher', hashed_password=get_password_hash('teacher'), role='teacher')
    db.add(teacher_user)

student_login = db.query(models.User).filter(models.User.username == 'student1').first()
if not student_login:
    student_login = models.User(username='student1', hashed_password=get_password_hash('student1'), role='student')
    db.add(student_login)

db.commit()
db.close()
print('Initial users created!')
