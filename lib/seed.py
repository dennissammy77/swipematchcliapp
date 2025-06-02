#!/usr/bin/env python3

from faker import Faker
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User, Company, Job, Application
from lib.base import Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///swipe_match_hired.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).delete()
    session.query(Company).delete()
    session.query(Job).delete()
    session.query(Application).delete()
    fake = Faker()
    
    roles = ['applicant', 'employer']
    users = []
    for i in range(10):
        user = User(
            name=fake.unique.name(),
            email=fake.unique.email(),
            mobile=123456789,
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

    jobs = []
    for _ in range(20):
        job = Job(
            name=fake.job(),
            salary=random.randint(50000, 200000),
            company=random.choice(companies)
        )
        session.add(job)
        session.commit()
        jobs.append(job)
        
    
    users = session.query(User).all()
    jobs = session.query(Job).all()
    statuses = ['applied', 'interviewing', 'rejected', 'offered','accepted']

    applications = []
    for _ in range(20):  # Generate 20 applications
        user = random.choice(users)
        job = random.choice(jobs)

        application = Application(
            user_id=user.id,
            job_id=job.id,
            status=random.choice(statuses),
            date=fake.date_time_between(start_date='-30d', end_date='now')
        )
        applications.append(application)

    session.bulk_save_objects(applications)
    session.commit()
        
    print("🌱 Seeding complete!")   
