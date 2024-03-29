import uuid

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.models.company import Company
from app.types.enums.job_application import JobApplicationStatus


class JobApplication(db.Model):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(JobApplicationStatus), nullable=False, default=JobApplicationStatus.saved
    )

    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id"), nullable=False
    )
    company: Mapped["Company"] = relationship("Company")
