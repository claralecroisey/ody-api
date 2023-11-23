from unittest.mock import patch

from flask import g

from app.models.company import Company
from app.models.job_application import JobApplication
from app.types.dtos.job_application import JobApplicationData
from app.types.enums.job_application import JobApplicationStatus
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
        company = CompanyFactory.create()
        job = JobApplicationFactory.create(user_id="mocked_user_id", company=company)

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

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_create_job_application(self, _, __, client, test_db):
        company = CompanyFactory.create()
        payload_body = {
            "title": "mocked_title",
            "description": "mocked_description",
            "company_name": company.name,
            "role": "mocked_role",
            "url": "mocked_url",
            "status": "applied",
        }
        response = client.post("/job-applications", json=payload_body)

        created_job = JobApplication.query.filter_by(
            user_id="mocked_user_id", title="mocked_title"
        ).first()
        assert created_job is not None
        assert response.status_code == 201

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_create_job_application_with_unknown_company_name_creates_company(
        self, _, __, client, test_db
    ):
        payload_body = {
            "title": "mocked_title",
            "description": "mocked_description",
            "company_name": "new_company_name",  # Creating a job application with a new company name
            "role": "mocked_role",
            "url": "mocked_url",
            "status": "applied",
        }
        client.post("/job-applications", json=payload_body)

        created_company = Company.query.filter_by(name="new_company_name").first()
        assert created_company is not None

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_update_job_application(self, _, __, client, test_db):
        job = JobApplicationFactory.create(
            user_id="mocked_user_id", company=CompanyFactory.create()
        )
        payload_body = {
            "title": "updated_title",
            "description": "updated_description",
            "status": "in_process",
        }
        response = client.put(f"/job-applications/{job.id}", json=payload_body)

        updated_job = JobApplication.query.get(job.id)
        assert response.status_code == 200
        assert updated_job is not None
        assert updated_job.title == "updated_title"
        assert updated_job.description == "updated_description"
        assert updated_job.status == JobApplicationStatus.in_process

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_update_job_application_returns_404_if_user_does_not_own_job_application(
        self, _, __, client, test_db
    ):
        different_user = UserFactory.create(id="different_user_id")
        # Job application is owned by another user (different user_id)
        job = JobApplicationFactory.create(
            user_id=different_user.id, company=CompanyFactory.create()
        )
        payload_body = {
            "title": "updated_title",
            "description": "updated_description",
            "status": "in_process",
        }
        response = client.put(f"/job-applications/{job.id}", json=payload_body)

        assert response.status_code == 404
        assert response.json["message"] == "Job application not found"

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_delete_user_job_application(self, _, __, client, test_db):
        job = JobApplicationFactory.create(
            user_id="mocked_user_id", company=CompanyFactory.create()
        )
        response = client.delete(f"/job-applications/{job.id}")

        assert JobApplication.query.get(job.id) is None
        assert response.status_code == 200

    @patch(
        "security.guards.auth0_service.validate_jwt",
        return_value={"sub": "google-oauth2|mocked_user_id"},
    )
    @patch(
        "security.guards.get_bearer_token_from_request",
        return_value="mocked_user_id",
    )
    def test_delete_job_application_returns_404_if_user_does_not_own_job_application(
        self, _, __, client, test_db
    ):
        different_user = UserFactory.create(id="different_user_id")
        # Job application is owned by another user (different user_id)
        job = JobApplicationFactory.create(
            user_id=different_user.id, company=CompanyFactory.create()
        )

        response = client.delete(f"/job-applications/{job.id}")
        assert response.status_code == 404
        assert response.json["message"] == "Job application not found"
