# cli.py
import click
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sqlalchemy as sa

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
@click.option('--user-id', prompt="User ID to Fetch and display details")
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

# @cli.command()
# @click.option('--user-id', prompt='User ID')
# def list_user_applications(user_id):
#     """📨 List all applications for a specific user"""
#     user = session.query(User).filter_by(id=user_id).first()

#     if not user:
#         console.print(f"[red]User with ID {user_id} not found.[/red]")
#         return
    
#     print(user)

#     apps = session.query(Application).filter_by(job_id=int(15)).all()
#     print(apps)
#     # apps = [app for app in apps if app.job_id == 15]
#     # print(apps)

#     if not apps:
#         console.print(f"[yellow]No applications found for user '{user.name}' (ID: {user_id})[/yellow]")
#         return

#     table = Table(title=f"Applications for {user.name}")
#     table.add_column("Application ID", justify="right")
#     table.add_column("Job Title")
#     table.add_column("Company")
#     table.add_column("Salary")
#     table.add_column("Status")
#     table.add_column("Date")

#     for app in apps:
#         job = app.job
#         company = job.company if job and job.company else None
#         table.add_row(
#             str(app.id),
#             job.name if job else "N/A",
#             company.name if company else "N/A",
#             f"${job.salary:,.2f}" if job and job.salary else "N/A",
#             app.status,
#             app.date.strftime("%Y-%m-%d")
#         )

#     console.print(table)
     
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
    try:
        """🏢 Create a company"""
        company = Company(name=name, industry=industry, website=website)
        session.add(company)
        session.commit()
        console.print(f"✅ [green]Company '{name}' created with ID: {company.id}[/]")
    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error:[/] {e}")

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
@click.option('--company-id', prompt="Company ID to fetch details")
def fetch_company(company_id):
    """🏭 Fetch and display company details"""
    company = session.query(Company).filter_by(id=company_id).first()

    if not company:
        console.print(f"[red]❌ Company with ID {company_id} not found.[/red]")
        return

    table = Table(title=f"Company Details (ID: {company.id})")
    table.add_column("Field")
    table.add_column("Value")
    
    #  table row details
    table.add_row("Name", company.name)
    table.add_row("Industry", company.industry)
    table.add_row("Website", company.website)
    
    console.print(table)

@cli.command()
@click.option('--company-id', prompt="Company ID to update")
def update_company(company_id):
    """✏️ Update company details"""
    company = session.query(Company).filter_by(id=company_id).first()

    if not company:
        console.print(f"[red]❌ Company with ID {company_id} not found.[/red]")
        return

    console.print(f"[cyan]Updating Company: {company.name} ({company.website})[/cyan]")

    try:
        new_name = click.prompt("New name", default=company.name, show_default=True)
        new_industry = click.prompt("New industry", default=company.industry, show_default=True)
        new_website = click.prompt("New website", default=company.website, show_default=True)

        # Update with validation
        company.name = new_name
        company.industry = new_industry
        company.website = new_website

        session.commit()
        console.print(f"[green]✅ Company '{company.name}' updated successfully.[/green]")

    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Validation error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error:[/] {e}")

@cli.command()
@click.option('--company-id', prompt="Company ID to update")
def delete_company(company_id):
    """❌ Delete a company"""
    company = session.query(Company).filter_by(id=company_id).first()

    if not company:
        console.print(f"[red]❌ Company with ID {company_id} not found.[/red]")
        return

    confirm = click.confirm(f"Are you sure you want to delete company '{company.name}' (ID: {company_id})?", default=False)
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return

    try:
        session.delete(company)
        session.commit()
        console.print(f"[green]Company '{company.name}' deleted successfully.[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]Error deleting company: {e}[/red]")



@cli.command()
@click.option('--title', prompt='Job title')
@click.option('--description', prompt='Job description')
@click.option('--Location', prompt='Job Location')
@click.option('--salary', prompt='Salary', type=float)
@click.option('--type', prompt='Contract type (full-time | part-time | contract | internship)')
@click.option('--company_id', prompt='Company ID', type=int)
def create_job(title, description, location, salary, type, company_id):
    """💼 Create a job listing"""
    try:
        job = Job(name=title, description=description, location=location, salary=salary, type=type, company_id=company_id)
        session.add(job)
        session.commit()
        console.print(f"✅ [green]Job '{title}' created with ID: {job.id}[/]")
    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error:[/] {e}")

@cli.command()
@click.option('--job-id', prompt='Job ID to update', type=int)
def update_job(job_id):
    """✏️ Update a job listing"""
    job = session.query(Job).filter_by(id=job_id).first()

    if not job:
        console.print(f"[red]Job with ID {job_id} not found.[/red]")
        return

    console.print(f"[cyan]Updating job: {job.name} (ID: {job.id})[/cyan]")

    try:
        new_name = click.prompt("New title", default=job.name, show_default=True)
        new_description = click.prompt("New description", default=job.description, show_default=True)
        new_location = click.prompt("New location", default=job.location, show_default=True)
        new_salary = click.prompt("New salary", default=job.salary, type=float, show_default=True)
        new_type = click.prompt("New type (full-time | part-time | contract | internship)", default=job.type, show_default=True)

        # Update fields with validation
        job.name = new_name
        job.description = new_description
        job.location = new_location
        job.salary = new_salary
        job.type = new_type.lower()

        session.commit()
        console.print(f"[green]Job '{job.name}' updated successfully.[/green]")

    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Validation Error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected Error:[/] {e}")

@cli.command()
@click.option('--job-id', prompt='Job ID to delete', type=int)
def delete_job(job_id):
    """❌ Delete a job"""
    job = session.query(Job).filter_by(id=job_id).first()

    if not job:
        console.print(f"[red]Job with ID {job_id} not found.[/red]")
        return

    confirm = click.confirm(f"Are you sure you want to delete job '{job.name}' (ID: {job_id})?", default=False)
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return

    try:
        session.delete(job)
        session.commit()
        console.print(f"[green]User '{job.name}' deleted successfully.[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]Error deleting user: {e}[/red]")

@cli.command()
def list_jobs():
    """🧾 List all jobs"""
    jobs = session.query(Job).all()
    table = Table(title="Jobs")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Location")
    table.add_column("Salary")
    table.add_column("Contract Type")
    table.add_column("Company ID")
    table.add_column("Company Name")

    for job in jobs:
        company = job.company
        table.add_row(
            str(job.id), 
            job.name, 
            job.description if job.description else "N/A", 
            job.location if job.location else "N/A", 
            f"${job.salary:,.2f}", 
            job.type if job.type else "N/A", 
            str(job.company_id),
            company.name if company else "N/A",
        )

    console.print(table)

@cli.command()
@click.option('--job-id', prompt='Job ID to fetch and Display details')
def fetch_job(job_id):
    """🏭 Fetch and display company details"""
    job = session.query(Job).filter_by(id=job_id).first()

    if not job:
        console.print(f"[red]Job with ID {job_id} not found.[/red]")
        return

    table = Table(title=f"Job Details (ID: {job.id})")
    table.add_column("Field")
    table.add_column("Value")
    
    #  table row details
    table.add_row("Title", job.name)
    table.add_row("Description", job.description if job.description else "N/A")
    table.add_row("Location", job.location if job.location else "N/A")
    table.add_row("Salary", f"${job.salary:,.2f}")
    table.add_row("Contract Type", job.type if job.type else "N/A")
    table.add_row("Company ID", str(job.company.id))
    table.add_row("Company Name", job.company.name if job.company else "N/A")
    
    console.print(table)



@cli.command()
@click.option('--user_id', prompt='User ID')
@click.option('--job_id', prompt='Job ID')
@click.option('--status', prompt='Application status')
def create_application(user_id, job_id, status):
    """📨 Create a job application"""
    try:
        print(user_id, job_id, status)
        app = Application(user_id=int(user_id), job_id=int(job_id), status=status)
        session.add(app)
        session.commit()
        console.print(f"✅ [green]Application submitted by User {user_id} for Job {job_id}[/]")
    except ValueError as ve:
        session.rollback()
        console.print(f"[bold red]Error:[/] {ve}")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error:[/] {e}")

@cli.command()
@click.option('--application_id', prompt='Application ID')
def fetch_application(application_id):
    """🔍 Fetch a specific application"""
    app = session.query(Application).filter_by(id=application_id).first()

    if not app:
        console.print(f"[red]Application with ID {application_id} not found.[/red]")
        return

    job = app.job
    user = app.user
    
    table = Table(title=f"Application Details (ID: {user.id})")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("User Id", str(user.id))
    table.add_row("User Name", user.name)
    table.add_row("Job Id", str(job.id))
    table.add_row("Job Name", job.name)
    table.add_row("Status", app.status)
    table.add_row("Date", app.date.strftime('%Y-%m-%d'))
    
    console.print(table)
    
@cli.command()
def list_applications():
    """📄 List all applications"""
    apps = session.query(Application).all()
    table = Table(title="Applications")
    table.add_column("ID", justify="right")
    table.add_column("User ID")
    table.add_column("User Name")
    table.add_column("Job ID")
    table.add_column("Job Name")
    table.add_column("Status")
    table.add_column("Date")
    

    for a in apps:
        print(a.id)
        print(a.job)
        print(a.user)
        user = a.user
        job = a.job
        table.add_row(
            str(a.id),
            str(a.user_id),
            user.name,
            str(a.job_id),
            job.name,
            a.status,
            a.date.strftime("%Y-%m-%d")
        )

    console.print(table)

@cli.command()
@click.option('--application_id', prompt='Application ID', type=int)
def update_application(application_id):
    """✏️ Update an application"""
    app = session.query(Application).filter_by(id=application_id).first()

    if not app:
        console.print(f"[red]Application with ID {application_id} not found.[/red]")
        return

    console.print(f"[cyan]Updating Application #{application_id}[/cyan]")

    try:
        new_status = click.prompt("New status", default=app.status, show_default=True)
        app.status = new_status  # Triggers @property validation
        session.commit()
        console.print(f"[green]Application #{application_id} updated successfully.[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]Error updating application: {e}[/red]")


@cli.command()
@click.option('--application_id', prompt='Application ID', type=int)
def delete_application(application_id):
    """❌ Delete an application"""
    app = session.query(Application).filter_by(id=application_id).first()

    if not app:
        console.print(f"[red]Application with ID {application_id} not found.[/red]")
        return

    confirm = click.confirm(f"Are you sure you want to delete application #{application_id}?", default=False)

    if confirm:
        session.delete(app)
        session.commit()
        console.print(f"[green]Application #{application_id} deleted successfully.[/green]")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")

if __name__ == '__main__':
    cli.add_command(create_user)
    cli.add_command(list_users)
    cli.add_command(update_user)
    cli.add_command(fetch_user)
    cli.add_command(delete_user)
    # cli.add_command(list_user_applications)
    
    cli.add_command(create_job)
    cli.add_command(list_jobs)
    cli.add_command(fetch_job)
    cli.add_command(update_job)
    cli.add_command(delete_job)
    
    cli.add_command(create_company)
    cli.add_command(list_companies)
    cli.add_command(fetch_company)
    cli.add_command(update_company)
    cli.add_command(delete_company)
        
    cli.add_command(create_application)
    cli.add_command(list_applications)
    cli.add_command(fetch_application)
    cli.add_command(update_application)
    cli.add_command(delete_application)
    
    cli()
    