from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes import auth, student, marks, result

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SRMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(student.router, prefix="/api")
app.include_router(marks.router, prefix="/api")
app.include_router(result.router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
