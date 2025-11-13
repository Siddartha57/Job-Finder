from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import search_jobs,upsert_jobs, delete_expired_jobs
from ..models import Job
from ..schemas import JobBase
from typing import List
from ..jobs_fetcher import fetch_jobs

router = APIRouter()

@router.get("/search", response_model=List[JobBase])
def search(keyword: str = "", location: str = "", db: Session = Depends(get_db)):
    return search_jobs(db, keyword, location)

@router.get("/fetch-now")
async def fetch_now(db: Session = Depends(get_db)):
    jobs = await fetch_jobs()
    upsert_jobs(db, jobs)
    delete_expired_jobs(db)

    return {"message": "Jobs fetched successfully", "count": len(jobs)}

@router.get("/all-jobs", response_model=List[JobBase])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

