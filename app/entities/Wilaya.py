from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Wilaya(Base):
    __tablename__ = 'wilayas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  
    latitude = Column(String)  
    longitude = Column(String)  
    zone_id = Column(Integer, ForeignKey('zones.id'))  

    zone = relationship("Zone", back_populates="wilayas") #option chaba pour eviter les jointures manuelles
    