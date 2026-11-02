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
git clone <repo-url>
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
4. Run `python manage.py migrate`
5. Start the app with `python manage.py runserver`
6. Create or update migrations when model files change

## Final Notes

This repository is designed for local development with a lightweight SQLite database. It is a good default for the team until the project needs a production-ready or shared database setup.

If your team wants, the next step could be adding a `.env` file and switching the project to a shared MySQL/PostgreSQL configuration for development and deployment.
