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
    try:
        user = User(name=name, email=email, mobile=mobile, role=role)
        session.add(user)
        session.commit()
        console.print(f"[green]User '{user.name}' created with ID: {user.id}[/]")
    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error:[/] {e}")
        
@click.command()
@click.option('--user-id', prompt="User ID to update")
def update_user(user_id):
    """➕ Update user account"""
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        console.print(f"[red]User with ID {user_id} not found.[/red]")
        return

    console.print(f"[cyan]Updating user: {user.name} ({user.email})[/cyan]")

    try:
        new_name = click.prompt("New name", default=user.name, show_default=True)
        new_email = click.prompt("New email", default=user.email, show_default=True)
        new_mobile = click.prompt("New mobile number", default=str(user.mobile), show_default=True)
        new_role = click.prompt("New role (applicant/employer)", default=user.role, show_default=True)

        # Update fields
        user.name = new_name
        user.email = new_email
        user.mobile = new_mobile
        user.role = new_role.lower()

        session.commit()
        console.print(f"[green]User '{user.name}' updated successfully.[/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[red]Error updating user: {e}[/red]")
        
@click.command()
@click.option('--user-id', prompt="User ID to fetch details")
def fetch_user(user_id):
    """👤 Fetch and display user details"""
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        console.print(f"[red]User with ID {user_id} not found.[/red]")
        return

    table = Table(title=f"User Details (ID: {user.id})")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Name", user.name)
    table.add_row("Email", user.email)
    table.add_row("Mobile", str(user.mobile))
    table.add_row("Role", user.role)

    console.print(table)

@cli.command()
@click.option('--user-id', prompt='User ID', type=int)
def list_user_applications(user_id):
    """📨 List all applications for a specific user"""
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        console.print(f"[red]User with ID {user_id} not found.[/red]")
        return

    apps = session.query(Application).filter_by(user_id=user_id).all()

    if not apps:
        console.print(f"[yellow]No applications found for user '{user.name}' (ID: {user_id})[/yellow]")
        return

    table = Table(title=f"Applications for {user.name}")
    table.add_column("Application ID", justify="right")
    table.add_column("Job Title")
    table.add_column("Company")
    table.add_column("Salary")
    table.add_column("Status")
    table.add_column("Date")

    for app in apps:
        job = app.job
        company = job.company if job and job.company else None
        table.add_row(
            str(app.id),
            job.name if job else "N/A",
            company.name if company else "N/A",
            f"${job.salary:,.2f}" if job and job.salary else "N/A",
            app.status,
            app.date.strftime("%Y-%m-%d")
        )

    console.print(table)
     
@cli.command()
@click.option('--user-id', prompt='User ID to delete', type=int)
def delete_user(user_id):
    """❌ Delete a user"""
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        console.print(f"[red]User with ID {user_id} not found.[/red]")
        return

    confirm = click.confirm(f"Are you sure you want to delete user '{user.name}' (ID: {user_id})?", default=False)
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return

    try:
        session.delete(user)
        session.commit()
        console.print(f"[green]User '{user.name}' deleted successfully.[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]Error deleting user: {e}[/red]")

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
    cli.add_command(create_user)
    cli.add_command(create_company)
    cli.add_command(create_job)
    cli.add_command(create_application)
    cli.add_command(list_users)
    cli.add_command(list_companies)
    cli.add_command(list_jobs)
    cli.add_command(list_applications)
    cli.add_command(update_user)
    cli.add_command(fetch_user)
    cli.add_command(delete_user)
    cli.add_command(list_user_applications)
    
    cli()
    
