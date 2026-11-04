# CSCI-4250 Project JobSite

A Django-based job board application for students and faculty. This repository is set up as a standard Django project with a custom user model and a SQLite development database by default.

## Tech Stack

- Python 3.10+
- Django 5.2.18
- SQLite for local development
- Django auth system with a custom `User` model

## Project Structure

- `accounts/` - custom user model and account-related logic
- `jobs/` - job-related models and functionality
- `config/` - Django project settings and URL config
- `manage.py` - Django management entry point
- `requirements.txt` - Python dependencies
- `db.sqlite3` - local SQLite database file created during setup
- `JobSite.sql` - legacy SQL reference file, not the active Django database setup

## Prerequisites

Before starting, make sure you have:

- Python installed
- Git installed
- A terminal or shell

## 1. Clone the Repository

```bash
git clone https://github.com/Blueboxdriver/CSCI-4250_Project_JobSite.git
cd CSCI-4250_Project_JobSite
```

## 2. Create a Virtual Environment

From the project root:

```bash
python -m venv .venv
```

Activate it:

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Set Up the Database

First generate a private local Django key (once per checkout). This command works in an activated virtual environment on Linux, macOS, and Windows and refuses to overwrite an existing `.env` file:

```bash
python -c "from pathlib import Path; from django.core.management.utils import get_random_secret_key; f = Path('.env').open('x'); f.write('DJANGO_SECRET_KEY=' + get_random_secret_key() + '\n'); f.close()"
```

If `.env` already exists, preserve it and add a `DJANGO_SECRET_KEY` value generated with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Settings load `.env` automatically; an existing environment variable takes precedence. Missing or blank keys stop startup with a configuration error. Keep the same private key across server restarts so sessions remain valid. `.env` is ignored by Git; never commit it or share its value.

The previously committed development key is retired. Replacing it invalidates existing signed sessions; users can sign in again. This does not change passwords or stored profiles. These settings remain for local development (`DEBUG=True`), not a production deployment.

This project is currently configured to use SQLite for local development. The database settings are in `config/settings.py` and point to a local file named `db.sqlite3` in the project root.

Run the migrations:

```bash
python manage.py migrate
```

If this is the first time setting up the project, Django will create the database file automatically.

## 5. Create a Superuser (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## 6. Run the Development Server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

For the admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Load Fictional Development Data

With the virtual environment active and Django running in debug mode, create a sample student, faculty user, student profile, and job posting with:

```bash
python manage.py seed_sample_data
```

The command is safe to rerun. It creates fictional records using `example.test` email addresses. The sample accounts have unusable passwords and cannot log in.

Faculty can create job postings at `/jobs/create/`; the server assigns the posting to the signed-in faculty user. Student and anonymous requests are denied.

## Sprint 1 frontend/backend contract

Sprint 1 uses the existing Django HTML pages and form submissions, not JSON API endpoints. Forms submit to the routes below with a CSRF token; successful submissions redirect, and invalid submissions render the form with validation errors.

| Route | Purpose and access |
| --- | --- |
| `/accounts/signup/` | GET/POST student registration; creates the account and profile and signs in the student. |
| `/accounts/signup/faculty/` | GET/POST faculty registration; creates a pending faculty account and profile. |
| `/accounts/login/` | GET/POST email and password login. |
| `/accounts/logout/` | POST logout with CSRF token. |
| `/accounts/post-login/` | Redirect after login; pending faculty go to the approval notice. |
| `/accounts/faculty/pending/` | Approval notice (403 while pending); approved faculty redirect to jobs. |
| `/accounts/profile/student/` | GET/POST the signed-in student's own profile and seeking-employment status. |
| `/accounts/profile/faculty/` | GET/POST the approved faculty member's own profile. |
| `/accounts/students/` | GET active students seeking employment; approved faculty only. |
| `/accounts/students/<student_id>/` | GET a visible student's profile; approved faculty only. The identifier is the profile's database primary key. |
| `/jobs/` | GET all postings for signed-in users, including past, current, and future postings. |
| `/jobs/create/` | GET/POST job creation; approved faculty only. Ownership comes from the session. |

Student registration uses unprefixed fields from `StudentSignUpForm` and `StudentProfileForm`. Faculty registration uses `user-` and `profile-` prefixes. Continue using the existing forms and templates as the field contract; clients cannot assign account roles, profile owners, job owners, or faculty approval.

An administrator approves faculty records in `/admin/` by enabling `is_approved`. Registration alone does not grant faculty posting, student browsing, or faculty profile-editing access. Pending faculty remain able to view the general job list while signed in.

### Sprint 1 verification

Detailed field contracts, visibility rules, and the team acceptance checklist are in [docs/sprint1-backend.md](docs/sprint1-backend.md).

Run `python manage.py test` for registration/login/logout, admin approval, profile ownership and visibility, faculty authorization, job validation, CSRF rejection, and posting-to-browsing integration tests. Tests use a separate temporary database.

For team acceptance on a fresh development database: run migrations, create a superuser, register a student and a faculty member through the existing signup page, confirm faculty access is denied before approval, approve through the admin panel, create a posting, and view it as the student. Toggle the student's seeking-employment status and verify the faculty list/detail visibility changes. Review the pages with the frontend team before marking Sprint 1 Done.

## Common Development Commands

After pulling new changes, run these as needed:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py test
```

## Custom User Model Notes

This project uses a custom user model:

```python
AUTH_USER_MODEL = "accounts.User"
```

That means when working with the database, always make sure that the `accounts` app migrations are up to date before migrating the whole project.

If you ever run into migration issues on a fresh setup, try:

```bash
python manage.py makemigrations accounts jobs
python manage.py migrate
```

## Database Notes

### Current default setup

The project is currently configured for SQLite, which is the easiest option for local development and team setup.

### If you want to switch to MySQL later

The `requirements.txt` includes `mysqlclient`, so MySQL is possible, but it is not currently configured in `config/settings.py`.

If your team wants a shared MySQL database, update the `DATABASES` section in `config/settings.py` to use MySQL settings instead of SQLite.

The old `JobSite.sql` file appears to be a legacy prototype schema and should not be treated as the current Django database source of truth unless your team intentionally decides to revive it.

## Troubleshooting

### Module not found / environment issues

Make sure your virtual environment is active before running Django commands.

```bash
source .venv/bin/activate
```

### Migration errors

Delete the local SQLite database only if you are intentionally resetting the project and want a fresh start:

```bash
rm db.sqlite3
python manage.py migrate
```

### Permission or setup issues

Run a Django health check:

```bash
python manage.py check
```

## Recommended Team Workflow

1. Pull latest repo updates
2. Activate `.venv`
3. Install dependencies with `pip install -r requirements.txt`
4. Configure the private `DJANGO_SECRET_KEY` as described above
5. Run `python manage.py migrate`
6. Start the app with `python manage.py runserver`
7. Create or update migrations when model files change

## Final Notes

This repository is designed for local development with a lightweight SQLite database. It is a good default for the team until the project needs a production-ready or shared database setup.

Any shared database or production deployment requires a separate team decision.
