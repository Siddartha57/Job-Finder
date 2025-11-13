from fastapi import FastAPI
from .database import Base, engine
from .scheduler import start_scheduler
from .api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Search API")

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(router, prefix="/api")
