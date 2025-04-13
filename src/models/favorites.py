from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from src import models


class Favorites(models.Base):
    __tablename__ = 'user_favorites'

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    university_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(
            "universities.id",
            ondelete="CASCADE"
        )
    )

    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    created_at: so.Mapped[datetime] = so.mapped_column(sa.Date, default=datetime.now)
