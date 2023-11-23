from unittest.mock import patch

from flask import g

from app.types.dtos.job_application import JobApplicationData
from tests.factories import CompanyFactory, JobApplicationFactory, UserFactory


class TestJobApplicationsRoutes:
    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_get_job_applications_endpoint(self, _, __, client, test_db):
        user = UserFactory.create()
        company = CompanyFactory.create()
        job = JobApplicationFactory.create(user_id=user.id, company=company)

        response = client.get("/job-applications")

        # Check if the 'g.user_id' was set correctly
        assert g.user_id == "mocked_user_id"

        assert response.status_code == 200
        user_job_applications = response.json
        assert len(user_job_applications) == 1

        expected_job_application_data = JobApplicationData(
            id=job.id,
            title=job.title,
            description=job.description,
            company_name=job.company.name,
            role=job.role,
            url=job.url,
            status=job.status,
        )
        assert (
            JobApplicationData.from_dict(user_job_applications[0])
            == expected_job_application_data
        )
