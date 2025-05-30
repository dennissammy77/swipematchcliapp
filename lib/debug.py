#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User, Company, Job, Application
from lib.base import Base

fake = Faker()

if __name__ == '__main__':
    engine = create_engine('sqlite:///swipe_match_hired.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Fetch and print all users
    print("\n users:")
    for user in session.query(User).all():
        print(user)
    
    # Fetch and print all companies
    print("\n companies:")
    for company in session.query(Company).all():
        print(company)
        
    print("\n jobs:")
    for job in session.query(Job).all():
        print(job)
        
    print("\n applications:")
    for application in session.query(Application).all():
        print(application)

    # import ipdb; ipdb.set_trace()
