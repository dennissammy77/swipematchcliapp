import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import User, Company, Application, Job, engine
from lib.base import Base
from datetime import datetime

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(engine) # Create tables
    yield
    Base.metadata.drop_all(engine) # Drop tables after test
    
@pytest.fixture
def session(setup_db):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.query(Application).delete()
    session.query(Company).delete()
    session.query(Job).delete()
    session.query(User).delete()

    company = Company(name="Google", industry="Tech", website="https://google.com")
    session.add(company)
    session.flush()  # gets the company.id before commit

    job = Job(name="Software Engineer", salary=120000, company_id=company.id)
    user = User(name="Alice", email="alice@example.com", mobile="123456789", role="applicant")
    
    session.add_all([job, user])
    session.commit()
    
    yield session
    session.close()
    
def test_create_application(session):
    app = Application(
        user_id=1,
        job_id=1,
        status="applied",
        date=datetime.utcnow()
    )
    session.add(app)
    session.commit()

    result = session.query(Application).first()
    assert result is not None
    assert result.status == "applied"
    assert result.user_id == '1'
    assert result.job_id == '1'

def test_application_relationships(session):
    app = Application(
        user_id=1,
        job_id=1,
        status="interviewing",
        date=datetime.utcnow()
    )
    session.add(app)
    session.commit()

    loaded_app = session.query(Application).first()
    assert loaded_app.user.name == "Alice"
    assert loaded_app.job.name == "Software Engineer"