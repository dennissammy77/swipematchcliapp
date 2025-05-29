from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conftest import SQLITE_URL
from models import User

class TestUser:
    '''Class User in models.py'''

    # start session, reset db
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # add test data
    john_Doe = Game(
        name="John Doe",
        email="johndoe@gmail.com",
        mobile=759233322,
        role="applicant"
    )

    session.add(john_Doe)
    session.commit()

    def test_user_has_correct_attributes(self):
        '''has attributes "name", "email", "mobile", "role", .'''
        assert(
            all(
                hasattr(
                    TestUser.john_Doe, attr
                ) for attr in [
                    "id",
                    "name",
                    "email",
                    "mobile",
                    "role",
                    "created_at",
                    "updated_at"
                ]))
