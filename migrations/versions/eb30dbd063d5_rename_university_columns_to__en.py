"""Rename university columns to *_en

Revision ID: eb30dbd063d5
Revises: 728f7c5d7122
Create Date: 2025-04-30 14:52:59.883981

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'eb30dbd063d5'
down_revision: Union[str, None] = '728f7c5d7122'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('universities', 'name', new_column_name='name_en')
    op.alter_column('universities', 'description', new_column_name='description_en')
    op.alter_column('universities', 'country_name', new_column_name='country_name_en')
    op.alter_column('universities', 'scholarship_name', new_column_name='scholarship_name_en')
    op.alter_column('universities', 'scholarship_description', new_column_name='scholarship_description_en')
    op.alter_column('universities', 'scholarship_benefits', new_column_name='scholarship_benefits_en')
    op.alter_column('universities', 'application_steps', new_column_name='application_steps_en')
    op.alter_column('subjects', 'name', new_column_name='name_en')
    op.alter_column('specialties', 'name', new_column_name='name_en')
    op.alter_column('specialties', 'description', new_column_name='description_en')


def downgrade() -> None:
    op.alter_column('universities', 'name_en', new_column_name='name')
    op.alter_column('universities', 'description_en', new_column_name='description')
    op.alter_column('universities', 'country_name_en', new_column_name='country_name')
    op.alter_column('universities', 'scholarship_name_en', new_column_name='scholarship_name')
    op.alter_column('universities', 'scholarship_description_en', new_column_name='scholarship_description')
    op.alter_column('universities', 'scholarship_benefits_en', new_column_name='scholarship_benefits')
    op.alter_column('universities', 'application_steps_en', new_column_name='application_steps')
    op.alter_column('subjects', 'name_en', new_column_name='name')
    op.alter_column('specialties', 'name_en', new_column_name='name')
    op.alter_column('specialties', 'description_en', new_column_name='description')