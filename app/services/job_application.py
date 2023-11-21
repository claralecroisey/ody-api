from typing import List

from sqlalchemy.orm import joinedload

from app import db
from app.models.models import Company, JobApplication
from app.types.dtos.job_application import JobApplicationData


def create_job_application(user_id, data):
    # TODO add session management
    company = Company.query.filter_by(name=data["company_name"]).first()

    if not company:
        company = Company(name=data["company_name"])
        db.session.add(company)
        db.session.flush()

    job_application = JobApplication(
        title=data["title"],
        description=data["description"],
        company_id=company.id,
        role=data["role"],
        url=data["url"],
        user_id=user_id,
    )
    db.session.add(job_application)
    db.session.commit()


def get_user_job_applications(user_id: str) -> List[JobApplicationData]:
    job_applications_query = JobApplication.query.filter_by(user_id=user_id).options(
        joinedload(JobApplication.company)
    )
    job_applications = [
        JobApplicationData(
            id=j.id,
            title=j.title,
            description=j.description,
            company_name=j.company.name,
            role=j.role,
            url=j.url,
            status=j.status,
        )
        for j in job_applications_query
    ]

    return job_applications
