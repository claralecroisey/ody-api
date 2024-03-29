"""enrich job listing model + company model

Revision ID: 9258b32581dc
Revises: 96f33174ec46
Create Date: 2023-11-19 23:18:44.617433

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9258b32581dc"
down_revision = "96f33174ec46"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "company",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("job_listing", schema=None) as batch_op:
        batch_op.add_column(sa.Column("role", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("url", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("user_id", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("company_id", sa.UUID(), nullable=False))
        joblistingstatus_enum = postgresql.ENUM(
            "saved",
            "applied",
            "rejected",
            "in_process",
            "offer_rejected",
            "offer_accepted",
            "closed",
            "withdrawn",
            name="joblistingstatus",
            create_type=False,
        )
        joblistingstatus_enum.create(op.get_bind(), checkfirst=True)
        batch_op.add_column(
            sa.Column(
                "status",
                joblistingstatus_enum,
                nullable=False,
                default="saved",
            )
        )
        batch_op.create_foreign_key(None, "company", ["company_id"], ["id"])
        batch_op.create_foreign_key(None, "user", ["user_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("job_listing", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("status")
        batch_op.drop_column("company_id")
        batch_op.drop_column("user_id")
        batch_op.drop_column("url")
        batch_op.drop_column("role")

    op.drop_table("company")
    # ### end Alembic commands ###
