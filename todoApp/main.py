from fastapi import FastAPI
from database import engine
import models
from routers import auth, todos, health_check
import uvicorn
import multiprocessing

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(health_check.router)
app.include_router(todos.router)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)
