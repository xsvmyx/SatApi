
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  

class Client(Base):
    __tablename__ = 'clients'

    
    client_id = Column(BigInteger, primary_key=True, index=True)  # identifiant métier
    etat_client = Column(String)
    bts_code = Column(String, ForeignKey('bts.code'))  # clé étrangère vers BTS.code

    bts = relationship("BTS", back_populates="clients")