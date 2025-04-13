from datetime import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as so

from src import models


class Chat(models.Base):
    __tablename__ = "chats"

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        primary_key=True
    )
    chat_name: so.Mapped[str] = so.mapped_column(
        sa.String
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime,
        default=datetime.utcnow
    )

    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    user = so.relationship("User", back_populates="chats", uselist=False)
    messages = so.relationship("ChatMessages", back_populates="chat")
