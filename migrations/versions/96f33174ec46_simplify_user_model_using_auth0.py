"""simplify user model using auth0

Revision ID: 96f33174ec46
Revises: eda5cf827261
Create Date: 2023-11-18 18:12:27.577212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96f33174ec46'
down_revision = 'eda5cf827261'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=False))
        batch_op.drop_column('content')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.drop_column('email')
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('job_listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('description')

    # ### end Alembic commands ###
