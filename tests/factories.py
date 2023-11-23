from factory import Faker, alchemy

from app import db
from app.models.company import Company
from app.models.models import JobApplication, User
from app.types.enums.job_application import JobApplicationStatus


class UserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class JobApplicationFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = JobApplication
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = Faker("job")
    description = Faker("paragraph")
    role = Faker("job")
    url = Faker("url")
    status = JobApplicationStatus.applied


class CompanyFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Company
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = Faker("company")
