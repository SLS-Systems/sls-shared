import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sls_shared.models.base import Base


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    service_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    referrer_name: Mapped[str | None] = mapped_column(String, nullable=True)
    referrer_organisation: Mapped[str | None] = mapped_column(String, nullable=True)
    referrer_email: Mapped[str | None] = mapped_column(String, nullable=True)
    referrer_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    local_authority: Mapped[str | None] = mapped_column(String, nullable=True)
    funding_body: Mapped[str | None] = mapped_column(String, nullable=True)
    prospect_first_name: Mapped[str] = mapped_column(String, nullable=False)
    prospect_last_name: Mapped[str] = mapped_column(String, nullable=False)
    prospect_dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    prospect_current_location: Mapped[str | None] = mapped_column(String, nullable=True)
    support_needs: Mapped[str | None] = mapped_column(Text, nullable=True)
    stage: Mapped[str] = mapped_column(String, nullable=False, default="enquiry")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    service = relationship("Service")
