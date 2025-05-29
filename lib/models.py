from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, Column, Integer, String, func, CheckConstraint, UniqueConstraint, DateTime 
from sqlalchemy.orm import relationship, backref
from lib.base import Base

engine = create_engine('sqlite:///swipe_match_hired.db')

# user
class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('email',name='unique_email'),
    )
    
    id = Column(Integer(),primary_key=True)
    name = Column(String())
    email = Column(String())
    mobile = Column(Integer())
    role = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'email={self.email})'
        
# company
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    industry = Column(String())
    website = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    def __repr__(self):
        return f'Company(id={self.id}, ' + \
            f'name={self.name}, '
    
    
# # job
# class Job(Base):
#     pass
# # application
# class Application(Base):
#     pass

    """_Relationships_
        user -> application (1-many)
        company -> job (1-many)
        job -> application (1-many)
    """