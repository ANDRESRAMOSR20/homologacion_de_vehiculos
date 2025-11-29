from sqlalchemy import Column, Integer, String, Boolean
from src.core.db.database import Base

class PartnerVehicle(Base):
    __tablename__ = "partner_vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, index=True)
    processed = Column(Boolean, default=False)
    match_id = Column(String, nullable=True)
