from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from base import Base

# user
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(),primary_key=True)
    name = Column(String())
    email = Column(String(), unique=True)
    mobile = Column(String())
    role = Column(String())
    pass
# company
class Company(Base):
    pass
# job
class Job(Base):
    pass
# application
class Application(Base):
    pass

    """_Relationships_
        user -> application (1-many)
        company -> job (1-many)
        job -> application (1-many)
    """