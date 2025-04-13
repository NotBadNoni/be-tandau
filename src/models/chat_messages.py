import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from src import models


class ChatMessages(models.Base):
    __tablename__ = 'chat_messages'

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True
    )

    chat_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False
    )

    user_message: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    answer_message: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime,
        default=datetime.datetime.utcnow
    )

    chat: so.Mapped["models.Chat"] = so.relationship("Chat", back_populates="messages", uselist=False)
