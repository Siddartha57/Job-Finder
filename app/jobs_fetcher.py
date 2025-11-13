import httpx
from dateutil import parser
from .config import settings

HEADERS = {
    "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
    "X-RapidAPI-Host": settings.RAPIDAPI_HOST
}

async def fetch_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    params = {
    "query": "fresher OR entry level OR trainee OR graduate software developer India",
    "page": "1"
}


    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)
        data = response.json().get("data", [])

        job_list = []
        for item in data:
            job_list.append({
                "external_id": item.get("job_id"),
                "title": item.get("job_title"),
                "company": item.get("employer_name"),
                "location": item.get("job_city"),
                "description": item.get("job_description"),
                "source_link": item.get("job_apply_link"),
                "registration_close_date": parser.parse(item["job_offer_expiration_date"]).date()
                    if item.get("job_offer_expiration_date") else None
            })

        return job_list
