from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  

class BTS(Base):
    __tablename__ = 'bts'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)             
    groupe = Column(String)                                      
    latitude = Column(Float)                             
    longitude = Column(Float)                             
    commune_id = Column(Integer, ForeignKey('communes.id'))

    commune = relationship("Commune", back_populates="bts")
