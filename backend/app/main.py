# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String
from fastapi import HTTPException

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    result = db.query(TaskModel).all()
    return [{"id": r.id, "title": r.title} for r in result]

@app.post("/tasks")
def add_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    new_task = TaskModel(title=task.title) 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"id": new_task.id, "title": new_task.title}


@app.put("/task")
def update_task(task: Task, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task.id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db.commit()
    db.refresh(db_task)
    return {"id": db_task.id, "title": db_task.title}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}
