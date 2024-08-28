from typing import Annotated
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Todos, Users
from ..database import SessionLocal
from loguru import logger
from .auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'user':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # if not bcrypt_context.verify(user_verification.password, user_model.hashed_pwd):
    #     raise HTTPException(status_code=500, detail="Error on password change.")

    if user_verification.password == user_verification.new_password:
        raise HTTPException(status_code=500, detail="Error on password change.")

    user_model.hashed_pwd = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

    logger.info("Change password successfully.")
