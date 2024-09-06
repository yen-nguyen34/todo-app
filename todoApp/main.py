from fastapi import FastAPI
import uvicorn
import multiprocessing

from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database import engine
import models
from routers import auth, todos, health_check, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="todoApp/templates")

app.mount("/static", StaticFiles(directory="todoApp/static"), name="static")


app.include_router(auth.router)
app.include_router(health_check.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)
