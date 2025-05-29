import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User, engine
from lib.base import Base

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(engine) # Create tables
    yield
    Base.metadata.drop_all(engine) # Drop tables after test
    
@pytest.fixture
def session(setup_db):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clean up database table beafore each test
    session.query(User).delete()
    session.commit()
    
    yield session
    session.close()

def test_user_has_correct_attributes(session):
    john_doe = User(
        name="John Doe",
        email="johndoe@gmail.com",
        mobile=759233322,
        role="applicant"
    )

    session.add(john_doe)
    session.commit()
    session.refresh(john_doe)

    for attr in [
        "id", "name", "email", "mobile", "role", "created_at", "updated_at"
    ]:
        assert hasattr(john_doe, attr)
    
def test_user_has_correct_values(session):
    # assert
    john_doe = User(
        name="John Doe",
        email="johndoe@gmail.com",
        mobile=759233322,
        role="applicant"
    )

    session.add(john_doe)
    session.commit()
    user = session.query(User).first()

    # Assert
    assert user.name == "John Doe"
    assert user.email == "johndoe@gmail.com"
    assert user.mobile == 759233322
    assert user.role == "applicant"
    assert user.id is not None  # Confirm it got an ID from the DB
