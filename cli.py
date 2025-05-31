# cli.py
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from lib.models import User, Company, Job, Application, engine

Session = sessionmaker(bind=engine)
session = Session()

def create_user():
    name = input("Enter user name: ")
    email = input("Enter email: ")
    mobile = input("Enter mobile: ")
    role = input("Enter role (applicant/employer): ")

    user = User(name=name, email=email, mobile=mobile, role=role)
    session.add(user)
    session.commit()
    print(f"✅ User '{name}' created with ID: {user.id}")

def list_users():
    users = session.query(User).all()
    print("\n📋 List of Users:")
    for user in users:
        print(f"{user.id}: {user.name} ({user.email}) - {user.role}")
    print()

def create_company():
    name = input("Company name: ")
    industry = input("Industry: ")
    website = input("Website: ")

    company = Company(name=name, industry=industry, website=website)
    session.add(company)
    session.commit()
    print(f"✅ Company '{name}' created with ID: {company.id}")

def list_companies():
    companies = session.query(Company).all()
    print("\n🏢 Companies:")
    for c in companies:
        print(f"{c.id}: {c.name} - {c.industry} ({c.website})")

def create_job():
    name = input("Job title: ")
    salary = float(input("Salary: "))
    company_id = int(input("Company ID: "))

    job = Job(name=name, salary=salary, company_id=company_id)
    session.add(job)
    session.commit()
    print(f"✅ Job '{name}' created with ID: {job.id}")

def list_jobs():
    jobs = session.query(Job).all()
    print("\n💼 Jobs:")
    for job in jobs:
        print(f"{job.id}: {job.name} - {job.salary} @ Company ID {job.company_id}")

def create_application():
    user_id = int(input("User ID: "))
    job_id = int(input("Job ID: "))
    status = input("Application status (applied/interviewing/accepted/rejected): ")

    app = Application(user_id=user_id, job_id=job_id, status=status, date=datetime.utcnow())
    session.add(app)
    session.commit()
    print(f"✅ Application created for user {user_id} to job {job_id}")

def list_applications():
    apps = session.query(Application).all()
    print("\n📄 Applications:")
    for a in apps:
        print(f"{a.id}: User {a.user_id} → Job {a.job_id} [{a.status}] on {a.date}")

def main_menu():
    while True:
        print("\n==== Job Application CLI ====")
        print("1. Create User")
        print("2. List Users")
        print("3. Create Company")
        print("4. List Companies")
        print("5. Create Job")
        print("6. List Jobs")
        print("7. Create Application")
        print("8. List Applications")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            create_company()
        elif choice == "4":
            list_companies()
        elif choice == "5":
            create_job()
        elif choice == "6":
            list_jobs()
        elif choice == "7":
            create_application()
        elif choice == "8":
            list_applications()
        elif choice == "9":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
