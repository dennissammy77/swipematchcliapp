#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User
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

    # import ipdb; ipdb.set_trace()
