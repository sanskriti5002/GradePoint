from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    roll_number = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    course = Column(String)
    
    marks = relationship('Mark', back_populates='student')

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    max_internal = Column(Float, default=30.0)
    max_external = Column(Float, default=70.0)
    
    marks = relationship('Mark', back_populates='subject')

class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    internal_marks = Column(Float, default=0.0)
    external_marks = Column(Float, default=0.0)

    student = relationship('Student', back_populates='marks')
    subject = relationship('Subject', back_populates='marks')
