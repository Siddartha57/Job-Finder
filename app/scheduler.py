from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends
from .jobs_fetcher import fetch_jobs
from .database import SessionLocal
from .crud import upsert_jobs, delete_expired_jobs
from datetime import datetime
from .config import settings

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

async def update_jobs_daily():
    db = SessionLocal()
    try:
        jobs = await fetch_jobs()
        upsert_jobs(db, jobs)
        delete_expired_jobs(db)
        print("Jobs updated:", len(jobs))
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(update_jobs_daily, CronTrigger(hour=0, minute=0))
    scheduler.start()
