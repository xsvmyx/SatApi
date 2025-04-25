from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Commune(Base):
    __tablename__ = 'communes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(String)
    longitude = Column(String)
    wilaya_id = Column(Integer, ForeignKey('wilayas.id'))

    wilaya = relationship("Wilaya", back_populates="communes")