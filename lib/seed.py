#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User, Company
from lib.base import Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///swipe_match_hired.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).delete()
    session.query(Company).delete()
    fake = Faker()
    
    roles = ['applicant', 'company','recruiter']
    users = []
    for i in range(10):
        user = User(
            name=fake.unique.name(),
            email=fake.unique.email(),
            mobile=fake.random_number(digits=9),
            role=random.choice(roles)
        )

        # add and commit individually to get IDs back
        session.add(user)
        session.commit()

        users.append(user)

    industries = ['Technology', 'Finance','DevOps', 'CyberSecurity']
    companies = []
    for i in range(10):
        company = Company(
            name=fake.unique.name(),
            industry=random.choice(industries),
            website=fake.url(),
        )

        # add and commit individually to get IDs back
        session.add(company)
        session.commit()

        companies.append(company)
        
    print("🌱 Seeding complete!")   
