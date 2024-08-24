from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from loguru import logger

router = APIRouter(prefix="/todo", tags=["All"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get("/all")
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/{todo_id}")
async def get_todo_id(db: db_dependency, todo_id: int = Path(gt=0), status_code=status.HTTP_200_OK):
    # try:
        todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
        if todo_model is not None:
            return todo_model
        logger.error(f"Not found for ${todo_id}")
        raise HTTPException(status_code=404, detail=f"Not found for ${todo_id}")
    # except Exception as e:
    #     logger.error(e)
    #     raise HTTPException(status_code=500, detail=str(e))



