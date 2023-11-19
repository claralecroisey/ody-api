import uuid
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.types.enums.job_listing import JobListingStatus


class JobListing(db.Model):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id"), nullable=False
    )
    status = mapped_column(
        Enum(JobListingStatus), nullable=False, default=JobListingStatus.saved
    )
