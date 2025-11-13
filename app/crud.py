from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from .models import Job

def upsert_jobs(db: Session, job_list: list):
    for j in job_list:
        existing = None
        if j.get("external_id"):
            existing = db.query(Job).filter(Job.external_id == j["external_id"]).first()

        if existing:
            existing.title = j["title"]
            existing.company = j.get("company")
            existing.location = j.get("location")
            existing.description = j.get("description")
            existing.registration_close_date = j.get("registration_close_date")
            existing.source_link = j.get("source_link")
            existing.updated_at = datetime.utcnow()
        else:
            db_job = Job(
                external_id=j.get("external_id"),
                title=j["title"],
                company=j.get("company"),
                location=j.get("location"),
                description=j.get("description"),
                registration_close_date=j.get("registration_close_date"),
                source_link=j.get("source_link"),
            )
            db.add(db_job)

    db.commit()

def delete_expired_jobs(db: Session):
    today = date.today()
    db.query(Job).filter(
        Job.registration_close_date != None,
        Job.registration_close_date < today
    ).delete()
    seven_days_ago = today - timedelta(days=7)

    db.query(Job).filter(
        Job.registration_close_date == None,
        Job.created_at < seven_days_ago
    ).delete()

    db.commit()

def search_jobs(db: Session, keyword: str, location: str):
    query = db.query(Job)

    if keyword:
        keyword = f"%{keyword.lower()}%"
        query = query.filter(func.lower(Job.title).like(keyword))
    
    if location:
        location = f"%{location.lower()}%"
        query = query.filter(func.lower(Job.location).like(location))
    
    return query.all()
