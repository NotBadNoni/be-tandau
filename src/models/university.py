import sqlalchemy as sa

from src.models import Base, TimestampMixin


class University(Base, TimestampMixin):
    __tablename__ = "universities"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False, index=True)
    image = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    scholarships = sa.Column(sa.Text, nullable=False)
    admissions = sa.Column(sa.Text, nullable=True)
    applications = sa.Column(sa.Text, nullable=False)
