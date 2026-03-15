import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from sls_shared.models.base import Base


class Supervision(Base):
    __tablename__ = "supervisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    supervisor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    supervision_type: Mapped[str] = mapped_column(String, nullable=False, default="one_to_one")
    status: Mapped[str] = mapped_column(String, nullable=False, default="scheduled")
    scheduled_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    discussion_points: Mapped[str | None] = mapped_column(Text, nullable=True)
    actions_agreed: Mapped[str | None] = mapped_column(Text, nullable=True)
    wellbeing_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    development_goals: Mapped[str | None] = mapped_column(Text, nullable=True)
    staff_comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    staff_member = orm_relationship("Profile", foreign_keys=[staff_id])
    supervisor = orm_relationship("Profile", foreign_keys=[supervisor_id])
