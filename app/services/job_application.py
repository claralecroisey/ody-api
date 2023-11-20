from app import db
from app.models.models import Company, JobApplication


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
