"""Updated Application class

Revision ID: bc1d36456021
Revises: 6b5b944cb7a7
Create Date: 2025-05-31 17:02:31.028308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1d36456021'
down_revision = '6b5b944cb7a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    # Drop applications_new if it exists (SQLite specific)
    conn.execute(sa.text('DROP TABLE IF EXISTS applications_new'))
    # Create new table with correct column types
    op.create_table(
        'applications_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=True),
        sa.Column('job_id', sa.Integer, nullable=True),
        # Add other columns here as they are in the current table
        # Example:
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
    )

    # Copy data from old table to new table, casting user_id and job_id to Integer
    conn.execute(sa.text('''
        INSERT INTO applications_new (id, user_id, job_id, status, date)
        SELECT id, CAST(user_id AS INTEGER), CAST(job_id AS INTEGER), status, date FROM applications
    '''))

    # Drop old table
    op.drop_table('applications')

    # Rename new table to old table's name
    op.rename_table('applications_new', 'applications')


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text('DROP TABLE IF EXISTS applications_old'))
    # Create old table with user_id and job_id as VARCHAR again
    op.create_table(
        'applications_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('job_id', sa.String(), nullable=True),
        # Add other columns here as they were originally
        # Example:
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
    )

    # Copy data back, casting to VARCHAR (TEXT in SQLite)
    conn.execute(sa.text('''
        INSERT INTO applications_old (id, user_id, job_id, status,date)
        SELECT id, CAST(user_id AS TEXT), CAST(job_id AS TEXT), status, date FROM applications
    '''))

    # Drop current table
    op.drop_table('applications')

    # Rename old table back
    op.rename_table('applications_old', 'applications')