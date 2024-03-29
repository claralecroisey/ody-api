"""add offer_received status in JobApplicationStatus enum

Revision ID: 50ab41d62e59
Revises: 8a0abd756e81
Create Date: 2023-11-22 20:30:29.403827

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "50ab41d62e59"
down_revision = "8a0abd756e81"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    job_application_status_enum = sa.Enum(
        "saved",
        "applied",
        "in_process",
        "rejected",
        "offer_rejected",
        "offer_accepted",
        "offer_received",
        "closed",
        "withdrawn",
        name="jobapplicationstatus",
    )

    # Create the new enum type
    job_application_status_enum.create(op.get_bind())

    # Alter the column to use the new enum type
    op.execute(
        "ALTER TABLE job_application "
        "ALTER COLUMN status TYPE jobapplicationstatus "
        "USING status::text::jobapplicationstatus"
    )
    # Drop the old enum type
    sa.Enum(
        "saved",
        "applied",
        "rejected",
        "in_process",
        "offer_rejected",
        "offer_accepted",
        "closed",
        "withdrawn",
        name="joblistingstatus",
    ).drop(op.get_bind())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "saved",
        "applied",
        "rejected",
        "in_process",
        "offer_rejected",
        "offer_accepted",
        "closed",
        "withdrawn",
        name="joblistingstatus",
    ).create(op.get_bind())
    with op.batch_alter_table("job_application", schema=None) as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.Enum(
                "saved",
                "applied",
                "in_process",
                "rejected",
                "offer_rejected",
                "offer_accepted",
                "offer_received",
                "closed",
                "withdrawn",
                name="jobapplicationstatus",
            ),
            type_=postgresql.ENUM(
                "saved",
                "applied",
                "rejected",
                "in_process",
                "offer_rejected",
                "offer_accepted",
                "closed",
                "withdrawn",
                name="joblistingstatus",
            ),
            existing_nullable=False,
        )

    sa.Enum(
        "saved",
        "applied",
        "in_process",
        "rejected",
        "offer_rejected",
        "offer_accepted",
        "offer_received",
        "closed",
        "withdrawn",
        name="jobapplicationstatus",
    ).drop(op.get_bind())
    # ### end Alembic commands ###
