"""Add user profile and preferences fields

Revision ID: 2025_07_01_0206
Revises: 
Create Date: 2025-07-01 02:06:29.316621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2025_07_01_0206'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum types first
    gender_enum = sa.Enum('MALE', 'FEMALE', 'NON_BINARY', 'PREFER_NOT_TO_SAY', name='gender')
    activity_enum = sa.Enum('SEDENTARY', 'LIGHTLY_ACTIVE', 'MODERATELY_ACTIVE', 'VERY_ACTIVE', 'EXTREMELY_ACTIVE', name='activitylevel')
    goal_enum = sa.Enum('LOSE_WEIGHT', 'MAINTAIN_WEIGHT', 'GAIN_WEIGHT', 'BUILD_MUSCLE', 'IMPROVE_ENERGY', name='goal')
    
    # Create the enum types in the database
    gender_enum.create(op.get_bind(), checkfirst=True)
    activity_enum.create(op.get_bind(), checkfirst=True)
    goal_enum.create(op.get_bind(), checkfirst=True)
    
    # Add columns with the enum types
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('gender', gender_enum, nullable=True))
    op.add_column('users', sa.Column('height_cm', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('weight_kg', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('dietary_restrictions', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('allergies', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('disliked_ingredients', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('preferred_cuisines', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('activity_level', activity_enum, nullable=True))
    op.add_column('users', sa.Column('goal', goal_enum, nullable=True))
    op.add_column('users', sa.Column('target_daily_calories', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('target_protein_g', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('target_carbs_g', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('target_fats_g', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('target_sodium_mg', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('target_sugar_g', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('weekly_budget_cents', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('onboarding_completed', sa.Boolean(), server_default=sa.text('false'), nullable=False))


def downgrade() -> None:
    # Drop columns
    op.drop_column('users', 'onboarding_completed')
    op.drop_column('users', 'weekly_budget_cents')
    op.drop_column('users', 'target_sugar_g')
    op.drop_column('users', 'target_sodium_mg')
    op.drop_column('users', 'target_fats_g')
    op.drop_column('users', 'target_carbs_g')
    op.drop_column('users', 'target_protein_g')
    op.drop_column('users', 'target_daily_calories')
    op.drop_column('users', 'goal')
    op.drop_column('users', 'activity_level')
    op.drop_column('users', 'preferred_cuisines')
    op.drop_column('users', 'disliked_ingredients')
    op.drop_column('users', 'allergies')
    op.drop_column('users', 'dietary_restrictions')
    op.drop_column('users', 'weight_kg')
    op.drop_column('users', 'height_cm')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'date_of_birth')
    
    # Drop enum types
    sa.Enum(name='gender').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='activitylevel').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='goal').drop(op.get_bind(), checkfirst=False)
