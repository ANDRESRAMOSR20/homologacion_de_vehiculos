from sqlalchemy import Column, String
from src.core.db.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
