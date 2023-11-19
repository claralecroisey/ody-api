from app import db
from app.models.models import Company, JobListing


def create_job_listing(user_id, data):
    # TODO add session management
    company = Company.query.filter_by(name=data["company_name"]).first()

    if not company:
        company = Company(name=data["company_name"])
        db.session.add(company)

    job_listing = JobListing(
        title=data["title"],
        description=data["description"],
        company_id=company.id,
        role=data["role"],
        url=data["url"],
        user_id=user_id,
    )
    db.session.add(job_listing)
    db.session.commit()
