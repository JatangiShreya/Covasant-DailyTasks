from sqlalchemy import Column,Integer,String,Text,DateTime,func
from config.postgresdb_config import Base

class App(Base):
    __tablename__="details"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),nullable=False)
    description=Column(Text)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
