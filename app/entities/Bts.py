from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  

class BTS(Base):
    __tablename__ = 'bts'

    #id = Column(Integer, primary_key=True, index=True)
    code = Column(String, primary_key=True, index=True)             
    #groupe = Column(String)                                      
    latitude = Column(Float)                             
    longitude = Column(Float)
    gen = Column(String)
    radius = Column(Integer)                             
    commune_id = Column(Integer, ForeignKey('communes.id'))
    nb_clients = Column(Integer, default=0)  
    age_moy = Column(Float,default=0)

    commune = relationship("Commune", back_populates="bts")
    clients = relationship("Client", back_populates="bts") 
