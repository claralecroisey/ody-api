from typing import Dict, List, Optional
from uuid import UUID

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
        status=data["status"],
    )
    db.session.add(job_application)
    db.session.commit()


def get_user_job_applications(user_id: str) -> List[JobApplicationData]:
    job_applications_query = (
        JobApplication.query.filter_by(user_id=user_id)
        .options(joinedload(JobApplication.company))
        .all()
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


def update_job_application(
    job_id: UUID, data: Dict[str, str]
) -> Optional[JobApplicationData]:
    job_application: JobApplication = JobApplication.query.get(job_id)
    if job_application is None:
        return

    job_application.title = data.get("title")
    job_application.description = data.get("description")
    job_application.status = data.get("status")

    db.session.commit()

    return JobApplicationData(
        id=job_application.id,
        title=job_application.title,
        description=job_application.description,
        company_name=job_application.company.name,
        role=job_application.role,
        url=job_application.url,
        status=job_application.status,
    )


def delete_job_application(job_id: UUID) -> None:
    job_application: JobApplication = JobApplication.query.get(job_id)
    if job_application is None:
        return

    db.session.delete(job_application)
    db.session.commit()


def check_user_owns_job_application(job_id: UUID, user_id: str) -> bool:
    job_application = JobApplication.query.get(job_id)
    return job_application is not None and job_application.user_id == user_id
