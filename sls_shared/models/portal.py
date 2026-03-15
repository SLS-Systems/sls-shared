import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship as orm_relationship

from sls_shared.models.base import Base


class PortalUser(Base):
    __tablename__ = "portal_users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    portal_type: Mapped[str] = mapped_column(String, nullable=False, default="family")
    organisation_name: Mapped[str | None] = mapped_column(String, nullable=True)
    professional_registration: Mapped[str | None] = mapped_column(String, nullable=True)
    is_primary_contact: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    invite_status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    invite_token: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    invite_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    invite_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PortalResidentAccess(Base):
    __tablename__ = "portal_resident_access"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portal_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("portal_users.id"), nullable=False)
    resident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("residents.id"), nullable=False)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    relationship: Mapped[str | None] = mapped_column(String, nullable=True)
    can_view_care_notes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_view_medications: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_health: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_documents: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_care_plans: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_risk_assessments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_full_care_plans: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_clinical_notes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_view_assessments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_add_professional_notes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_download_reports: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_message_staff: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    access_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PortalMessage(Base):
    __tablename__ = "portal_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    resident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("residents.id"), nullable=False)
    portal_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("portal_users.id"), nullable=False)
    sender_type: Mapped[str] = mapped_column(String, nullable=False)
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProfessionalNote(Base):
    __tablename__ = "professional_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False)
    resident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("residents.id"), nullable=False)
    portal_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("portal_users.id"), nullable=False)
    note_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    visit_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_reviewed_by_staff: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
