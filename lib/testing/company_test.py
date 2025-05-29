import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Company, engine
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
    session.query(Company).delete()
    session.commit()
    
    yield session
    session.close()
    
def test_row_has_correct_attr(session):
    google = Company(
        name="Google",
        industry="Technology",
        website="https://google.com"
    )
    
    session.add(google)
    session.commit()
    
    session.refresh(google)
    
    for attr in [
        "id", "name", "industry", "website"
    ]:
        assert hasattr(google, attr)
        
        
def test_row_has_correct_values(session):
    google = Company(
        name="Google",
        industry="Technology",
        website="https://google.com"
    )
    
    session.add(google)
    session.commit()
    
    session.refresh(google)
    # Assert
    assert google.name == "Google"
    assert google.industry == "Technology"
    assert google.website == "https://google.com"
    assert google.id is not None  # Confirm it got an ID from the DB
