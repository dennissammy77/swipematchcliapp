import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Job, Company, engine
from lib.base import Base

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(setup_db):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clean up both tables before each test
    session.query(Job).delete()
    session.query(Company).delete()
    session.commit()

    yield session
    session.close()


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
