import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from sls_shared.models.base import Base


class OncallRota(Base):
    __tablename__ = "oncall_rotas"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    service_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="manager")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    staff_member = orm_relationship("Profile", foreign_keys=[profile_id])


class OncallLog(Base):
    __tablename__ = "oncall_logs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    service_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    resident_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("residents.id"), nullable=True)
    oncall_profile_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    logged_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    caller_name: Mapped[str | None] = mapped_column(String, nullable=True)
    caller_role: Mapped[str | None] = mapped_column(String, nullable=True)
    call_reason: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    advice_given: Mapped[str | None] = mapped_column(Text, nullable=True)
    actions_taken: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[str] = mapped_column(String, nullable=False, default="resolved")
    escalated_to: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    call_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    call_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    follow_up_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    follow_up_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    oncall_person = orm_relationship("Profile", foreign_keys=[oncall_profile_id])
    logger = orm_relationship("Profile", foreign_keys=[logged_by])
    escalated_person = orm_relationship("Profile", foreign_keys=[escalated_to])
    resident = orm_relationship("Resident")


class EscalationChain(Base):
    __tablename__ = "escalation_chains"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    service_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    chain_type: Mapped[str] = mapped_column(String, nullable=False, default="general")
    steps: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
