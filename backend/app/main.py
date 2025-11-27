#imports
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Date
from datetime import date, datetime
from dotenv import load_dotenv

import os
from .gemini import Gemini


#Table 
class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    full_note = Column(String, nullable=True)
    due = Column(Date, nullable=False)

Base.metadata.create_all(bind=engine)

#Task model
class TaskBase(BaseModel):
    title: str
    description: str
    full_note: Optional[str] = None
    due: date

#Task create model
class TaskCreate(TaskBase):
    pass

#Optional Task updates
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    full_note: Optional[str] = None
    due: Optional[date] = None

#Read Orm for JSON
class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@app.post("/tasks", response_model=TaskOut)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        full_note=task.full_note,
        due=task.due
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.full_note is not None:
        db_task.full_note = task.full_note
    if task.due is not None:
        db_task.due = task.due
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}

@app.get("/plan-with-ai")
def plan_with_ai(db: Session = Depends(get_db)):
    # Fetch tasks from DB
    tasks = db.query(TaskModel).all()
    if not tasks:
        return {"plan": {}}

    # Initialize Gemini AI
    gemini_api_key = os.getenv("KEY")
    if not gemini_api_key:
        raise ValueError("KEY environment variable not set.")

    ai_platform = Gemini(api_key=gemini_api_key)
    today = datetime.today().date()

    # Generate the plan using the AI class
    plan_json = ai_platform.plan_tasks(tasks, start_date=today)

    return {"plan": plan_json}


