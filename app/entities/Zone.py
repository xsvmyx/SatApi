from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base 


class Zone(Base):
    __tablename__ = 'zones' 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  
    latitude = Column(String)  
    longitude = Column(String) 

    wilayas = relationship("Wilaya", back_populates="zone") 
    