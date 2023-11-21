from dataclasses import dataclass
from uuid import UUID

from dataclasses_json import DataClassJsonMixin

from app.types.enums.job_application import JobApplicationStatus


@dataclass
class JobApplicationData(DataClassJsonMixin):
    id: UUID
    title: str
    description: str
    company_name: str
    role: str
    url: str
    status: JobApplicationStatus
