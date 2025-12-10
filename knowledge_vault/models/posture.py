import uuid

from sqlalchemy import Column, Integer, DateTime, func, JSON, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from knowledge_vault.utils.database import Base

class Posture(Base):
    __tablename__ = "posture"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, default=uuid.uuid4)
    score = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="unknown")
    issues = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=func.now())