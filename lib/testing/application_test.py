import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from lib.models import User, Company, Application, Job, engine
from lib.base import Base
from datetime import datetime

Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    # Setup DB
    Base.metadata.create_all(engine)
    yield
    # Teardown DB
    engine.dispose()  # close all pooled connections
    Base.metadata.drop_all(engine)
    clear_mappers()  # clears class-to-table mappings to avoid lingering connections

@pytest.fixture(scope="function")
def session(setup_db):
    # Create a new session for each test
    session = Session()

    # Clean DB tables (order matters to respect FK constraints)
    session.query(Application).delete()
    session.query(Job).delete()
    session.query(User).delete()
    session.query(Company).delete()

    # Setup test data
    company = Company(name="Google", industry="Tech", website="https://google.com")
    session.add(company)
    session.flush()

    job = Job(name="Software Engineer", salary=120000, company_id=company.id)
    user = User(name="Alice", email="alice@example.com", mobile="759233322", role="applicant")
    print(user)
    session.add_all([job, user])
    session.commit()

    yield session

    # Close session after test
    session.close()

def test_create_application(session):
    users = session.query(User).all()
    user = session.query(User).first()
    job = session.query(Job).first()
    
    print(user,users)

    assert user is not None, "User not found in DB"
    assert job is not None, "Job not found in DB"
    
    app = Application(
        user_id=user.id,
        job_id=job.id,
        status="applied",
        date=datetime.utcnow()
    )
    session.add(app)
    session.commit()

    result = session.query(Application).first()
    assert result is not None
    assert result.status == "applied"
    assert result.user_id == user.id
    assert result.job_id == job.id
        
def test_application_relationships(session):
    user = session.query(User).first()
    job = session.query(Job).first()
    
    assert user is not None, "User not found in DB"
    assert job is not None, "Job not found in DB"
    
    app = Application(
        user_id=user.id,
        job_id=job.id,
        status="interviewing",
    )
    session.add(app)
    session.commit()

    loaded_app = session.query(Application).first()
    assert loaded_app.user.name == "Alice"
    assert loaded_app.job.name == "Software Engineer"
