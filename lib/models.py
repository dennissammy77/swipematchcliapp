from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, Column, Integer, String, func, CheckConstraint, UniqueConstraint, DateTime 
from sqlalchemy.orm import relationship, backref
from lib.base import Base
from datetime import datetime
import re

engine = create_engine('sqlite:///swipe_match_hired.db')

# user
class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('email',name='unique_email'),
    )
    
    id = Column(Integer, primary_key=True)
    _name = Column("name", String)
    _email = Column("email", String)
    _mobile = Column("mobile", Integer)
    _role = Column("role", String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    applications = relationship("Application", back_populates="user")
    
    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'email={self.email})'
            
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string.")
        email_regex = r'^\S+@\S+\.\S+$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        if not str(value).isdigit() or len(str(value)) < 10:
            raise ValueError("Mobile must be a valid number with at least 10 digits. Use format 759233322")
        self._mobile = int(value)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in ['applicant', 'employer']:
            raise ValueError("Role must be either 'applicant' or 'employer'.")
        self._role = value
        
# company
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    _name = Column("name", String())
    _industry = Column("industry", String())
    _website = Column("website", String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    jobs = relationship('Job', back_populates='company')
    
    def __repr__(self):
        return f'Company(id={self.id}, ' + \
            f'name={self.name}, '
            
    # Name validation
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Company name cannot be empty.")
        self._name = value.strip()

    # Industry validation
    @property
    def industry(self):
        return self._industry

    @industry.setter
    def industry(self, value):
        if not value or not value.strip():
            raise ValueError("Industry cannot be empty.")
        self._industry = value.strip()

    # Website validation
    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        if not value or not value.strip():
            raise ValueError("Website cannot be empty.")
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValueError("Website must start with http:// or https://")
        self._website = value.strip()
      
# # job
class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    _name = Column("name", String)
    _location = Column("location", String)
    _description = Column("description", String)
    _salary = Column("salary",Integer)
    _type = Column("type", String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    
    def __repr__(self):
        return f'Job(id={self.id}, ' + \
            f'name={self.name}, '
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Job name cannot be empty.")
        self._name = value.strip()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not value or not value.strip():
            raise ValueError("Job location cannot be empty.")
        self._location = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or not value.strip():
            raise ValueError("Job description cannot be empty.")
        self._description = value.strip()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        allowed_types = ['full-time', 'part-time', 'contract', 'internship']
        value = value.strip().lower()
        if value not in allowed_types:
            raise ValueError(f"Job type must be one of: {', '.join(allowed_types)}.")
        self._type = value

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Salary must be a positive number.")
        self._salary = value

# # application

class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    job_id = Column(String, ForeignKey('jobs.id'))
    status = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    
    def __repr__(self):
        return f'Application(id={self.id}, ' + \
            f'status={self.status}, '
    

"""_Relationships_
    user -> application (1-many)
    company -> job (1-many)
    job -> application (1-many)
"""