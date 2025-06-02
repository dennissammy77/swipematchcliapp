#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models import User, Company, Job, Application, engine
from lib.base import Base

Session = sessionmaker(bind=engine)
fake = Faker()

if __name__ == '__main__':
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
