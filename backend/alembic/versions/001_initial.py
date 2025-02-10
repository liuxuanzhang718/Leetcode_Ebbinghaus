"""initial

Revision ID: 001
Revises: 
Create Date: 2024-02-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('notification_time', sa.Time(), nullable=False),
        sa.Column('timezone', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create problems table
    op.create_table(
        'problems',
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('leetcode_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('first_study_date', sa.Date(), nullable=False),
        sa.Column('next_review_date', sa.Date(), nullable=False),
        sa.Column('stage', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('problem_id'),
        sa.UniqueConstraint('leetcode_number')
    )

    # Create review_logs table
    op.create_table(
        'review_logs',
        sa.Column('review_id', sa.Integer(), nullable=False),
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('review_date', sa.Date(), nullable=False),
        sa.Column('stage', sa.Integer(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.problem_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('review_id')
    )

    # Create indexes
    op.create_index(op.f('ix_problems_next_review_date'), 'problems', ['next_review_date'], unique=False)
    op.create_index(op.f('ix_review_logs_review_date'), 'review_logs', ['review_date'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_review_logs_review_date'), table_name='review_logs')
    op.drop_index(op.f('ix_problems_next_review_date'), table_name='problems')

    # Drop tables
    op.drop_table('review_logs')
    op.drop_table('problems')
    op.drop_table('users') 