import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from lib.models import User, Company, Application, Job, engine
from lib.base import Base

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

def test_company_has_correct_attr(session):
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
        
def test_company_has_correct_values(session):
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
    
def test_job_has_correct_attrs(session):
    company = Company(name="Google", industry="Tech", website="https://google.com")
    session.add(company)
    session.commit()
    session.refresh(company)

    job = Job(
        name="Software Engineer",
        location="Nairobi, Kenya",
        description="Senior engineer solving real-world problems",
        salary=200000,
        type="contract",
        company_id=company.id
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    for attr in [
        "id", "name", "location", "description", "salary", "type", "company_id"
    ]:
        assert hasattr(job, attr)


def test_job_has_correct_values(session):
    company = Company(name="Google", industry="Tech", website="https://google.com")
    session.add(company)
    session.commit()
    session.refresh(company)

    job = Job(
        name="Backend Developer",
        location="Remote",
        description="Build backend systems",
        salary=180000,
        type="full-time",
        company_id=company.id
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    assert job.name == "Backend Developer"
    assert job.location == "Remote"
    assert job.description == "Build backend systems"
    assert job.salary == 180000
    assert job.type == "full-time"
    assert job.company_id == company.id
    
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
        mobile="759233322",
        role="applicant"
    )

    session.add(john_doe)
    session.commit()
    session.flush()
    print('users',session.query(User).all())
    user = session.query(User).filter_by(
        id = john_doe.id
    ).first()
    print(user)
    # Assert
    assert user.name == john_doe.name
    assert user.email == john_doe.email
    assert user.mobile == john_doe.mobile
    assert user.role == john_doe.role
    assert user.id is not None  # Confirm it got an ID from the DB
