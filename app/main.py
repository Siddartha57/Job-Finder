from fastapi import FastAPI
from .database import Base, engine
from .scheduler import start_scheduler
from .api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Search API")

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(router, prefix="/api")
