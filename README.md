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

- Git and Python 3.10 or newer, with pip and virtual-environment support.
- A writable project folder. SQLite needs write access to both `db.sqlite3` and its containing folder.
- Linux: a terminal. Windows: PowerShell and a Python installation available through `py`.

SQLite requires no database server. The current requirements also include `mysqlclient`, so installing the full dependency list may require its native build dependencies even though the app uses SQLite.

## First-time setup: Linux

On Ubuntu/Debian, install the prerequisites below. Other distributions use different package names; see the [mysqlclient installation instructions](https://github.com/PyMySQL/mysqlclient#install).

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-dev default-libmysqlclient-dev build-essential pkg-config
```

From the folder where you keep projects:

```bash
git clone https://github.com/Blueboxdriver/CSCI-4250_Project_JobSite.git
cd CSCI-4250_Project_JobSite
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Generate a private local key **once per checkout**, then prepare the database and create your own admin login:

```bash
python -c "from pathlib import Path; from django.core.management.utils import get_random_secret_key; f = Path('.env').open('x'); f.write('DJANGO_SECRET_KEY=' + get_random_secret_key() + '\n'); f.close()"
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py test
python manage.py runserver
```

## First-time setup: Windows (PowerShell)

Install Python and Git, then open a new PowerShell window. Confirm `py --version` and `git --version` work. Run these commands from the folder where you keep projects:

```powershell
git clone https://github.com/Blueboxdriver/CSCI-4250_Project_JobSite.git
Set-Location CSCI-4250_Project_JobSite
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These instructions use the virtual environment's Python directly, so PowerShell script activation and execution-policy changes are unnecessary. If `mysqlclient` has no compatible binary wheel for your Python version/architecture, follow its [Windows build instructions](https://github.com/PyMySQL/mysqlclient#windows) before retrying dependency installation.

Generate a private local key **once per checkout**, then prepare the database and create your own admin login:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; from django.core.management.utils import get_random_secret_key; f = Path('.env').open('x'); f.write('DJANGO_SECRET_KEY=' + get_random_secret_key() + '\n'); f.close()"
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

## Open the app and approve faculty

Keep the server terminal open and visit [the homepage](http://127.0.0.1:8000/). Stop the server with **Ctrl+C**.

Register student/faculty accounts through the site. Sign in to see saved jobs on the homepage and Jobs page. A fresh database has no accounts or postings.

For faculty approval, open [Django admin](http://127.0.0.1:8000/admin/) and use the username/password you chose with `createsuperuser`. There is no default admin login. Open the faculty record, enable **Is approved**, and save. Then sign in as the faculty user and open Jobs → Create a job posting. A faculty registration alone does not grant those privileges.

## Run again after initial setup

Open a terminal in `CSCI-4250_Project_JobSite` (the folder containing `manage.py`). Keep the existing `.env` and database; do not recreate them each time.

Linux:

```bash
source .venv/bin/activate
python manage.py runserver
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

After pulling team changes, reinstall requirements and apply committed migrations before starting the server:

| Task | Linux (activated environment) | Windows PowerShell |
| --- | --- | --- |
| Dependencies | `python -m pip install -r requirements.txt` | `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| Migrations | `python manage.py migrate` | `.\.venv\Scripts\python.exe manage.py migrate` |
| Checks | `python manage.py check` | `.\.venv\Scripts\python.exe manage.py check` |
| Tests | `python manage.py test` | `.\.venv\Scripts\python.exe manage.py test` |
| Sample data | `python manage.py seed_sample_data` | `.\.venv\Scripts\python.exe manage.py seed_sample_data` |

## Private local configuration

The key-generation command refuses to overwrite an existing `.env`. If that file already exists, preserve it. If it lacks a key, generate one with the appropriate virtual-environment Python using `-c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`, then add `DJANGO_SECRET_KEY=<generated value>` to `.env` without angle brackets.

Settings load `.env` automatically; an existing environment variable takes precedence. Missing or blank keys stop startup. Keep the same private key across restarts. Replacing it invalidates existing signed sessions, requiring users to sign in again; it does not change passwords or saved profiles. Never commit `.env` or `db.sqlite3`; both are ignored by Git.

These instructions run the local development configuration (`DEBUG=True`), not a production deployment. Linux setup has been exercised on the development host; Windows commands have not been executed on a Windows machine.

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

On Linux with the environment activated, run these checks as needed. On Windows, replace `python` with `.\.venv\Scripts\python.exe`:

```bash
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

Apply the migrations already committed to the repository:

```bash
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

Linux: activate with `source .venv/bin/activate`. Windows: use `.\.venv\Scripts\python.exe` directly. Install requirements with that same interpreter. If Linux reports `No module named venv`, install your distribution's Python venv package. If Windows cannot find `py`, check your Python installation before continuing.

### Migration errors

Run `manage.py showmigrations` and `manage.py migrate` with your platform's virtual-environment Python. Do not delete the database or generate replacement migrations just to resolve a startup error; that can discard local data or diverge from the team's schema. Only use `makemigrations` when intentionally changing models, then commit and review the resulting migration.

### Read-only database

Run the server from a normal terminal with write access to the project folder and database. A server launched inside a read-only sandbox can display pages but cannot register accounts, save sessions, or publish jobs. Restart it with the required filesystem access; do not recreate the database.

### Missing key or existing .env

Follow Private local configuration above. `FileExistsError` from the one-time key command means `.env` already exists; preserve it rather than overwriting it.

### Port already in use

Stop your previous development server with Ctrl+C, or run `manage.py runserver 8001` using your platform's interpreter and open `http://127.0.0.1:8001/`.

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

On Windows, use `.\.venv\Scripts\python.exe` directly instead of activating the environment; use `-m pip` with that interpreter to install dependencies.

## Final Notes

This repository is designed for local development with a lightweight SQLite database. It is a good default for the team until the project needs a production-ready or shared database setup.

Any shared database or production deployment requires a separate team decision.
