# cli.py
import click
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from lib.models import User, Company, Job, Application, engine

Session = sessionmaker(bind=engine)
session = Session()

console = Console()

@click.group()
def cli():
    """📘 Job Tracker CLI App"""
    pass

@cli.command()
@click.option('--name', prompt='User name')
@click.option('--email', prompt='Email')
@click.option('--mobile', prompt='Mobile number')
@click.option('--role', prompt='Role (applicant/employer)')
def create_user(name, email, mobile, role):
    """➕ Create a new user"""
    user = User(name=name, email=email, mobile=mobile, role=role)
    session.add(user)
    session.commit()
    console.print(f"✅ [green]User '{name}' created with ID: {user.id}[/]")

@cli.command()
def list_users():
    """📋 List all users"""
    users = session.query(User).all()
    table = Table(title="Users")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Role")
    table.add_column("Mobile")

    for u in users:
        table.add_row(str(u.id), u.name, u.email, u.role, str(u.mobile))

    console.print(table)

@cli.command()
@click.option('--name', prompt='Company name')
@click.option('--industry', prompt='Industry')
@click.option('--website', prompt='Website')
def create_company(name, industry, website):
    """🏢 Create a company"""
    company = Company(name=name, industry=industry, website=website)
    session.add(company)
    session.commit()
    console.print(f"✅ [green]Company '{name}' created with ID: {company.id}[/]")

@cli.command()
def list_companies():
    """🏭 List all companies"""
    companies = session.query(Company).all()
    table = Table(title="Companies")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Industry")
    table.add_column("Website")

    for c in companies:
        table.add_row(str(c.id), c.name, c.industry, c.website)

    console.print(table)

@cli.command()
@click.option('--title', prompt='Job title')
@click.option('--salary', prompt='Salary', type=float)
@click.option('--company_id', prompt='Company ID', type=int)
def create_job(title, salary, company_id):
    """💼 Create a job listing"""
    job = Job(title=title, salary=salary, company_id=company_id)
    session.add(job)
    session.commit()
    console.print(f"✅ [green]Job '{title}' created with ID: {job.id}[/]")

@cli.command()
def list_jobs():
    """🧾 List all jobs"""
    jobs = session.query(Job).all()
    table = Table(title="Jobs")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Salary")
    table.add_column("Company ID")

    for job in jobs:
        table.add_row(str(job.id), job.name, f"${job.salary:,.2f}", str(job.company_id))

    console.print(table)

@cli.command()
@click.option('--user_id', prompt='User ID', type=int)
@click.option('--job_id', prompt='Job ID', type=int)
@click.option('--status', prompt='Application status')
def create_application(user_id, job_id, status):
    """📨 Create a job application"""
    app = Application(user_id=user_id, job_id=job_id, status=status, date=datetime.utcnow())
    session.add(app)
    session.commit()
    console.print(f"✅ [green]Application submitted by User {user_id} for Job {job_id}[/]")

@cli.command()
def list_applications():
    """📄 List all applications"""
    apps = session.query(Application).all()
    table = Table(title="Applications")
    table.add_column("ID", justify="right")
    table.add_column("User ID")
    table.add_column("Job ID")
    table.add_column("Status")
    table.add_column("Date")

    for a in apps:
        table.add_row(
            str(a.id),
            str(a.user_id),
            str(a.job_id),
            a.status,
            a.date.strftime("%Y-%m-%d")
        )

    console.print(table)

if __name__ == '__main__':
    cli()
