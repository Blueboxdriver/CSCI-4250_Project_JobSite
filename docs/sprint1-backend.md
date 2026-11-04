# Sprint 1 backend contract and acceptance

## Decisions

- Use Django-rendered HTML forms at `/accounts/...` and `/jobs/...`; draft `/api/...` routes are not required.
- Administrators approve each faculty registration before faculty privileges are granted.
- Faculty see only active student accounts with seeking employment enabled. Turning it off removes the profile from both the faculty list and detail access (404).
- Job browsing shows all postings, including past and future dates. Dates do not automatically close postings.
- Non-scholarship campus employment is a posting policy faculty must follow, not a separate eligibility field or approval workflow.
- Preserve the existing frontend wording and layout; frontend changes in this branch only add the employment-status indicator.

## Accounts and profile fields

Registration account fields are `username` (a valid email, normalized to lowercase and also stored as email), optional `first_name`/`last_name` (150 characters each), and required matching `password1`/`password2`. Django rejects duplicate usernames/emails and applies its configured password validators: similarity, minimum length, common-password and numeric-only checks. Passwords are hashed. Login uses `username` and `password` with case-normalized email. Logout is a CSRF-protected POST.

| Student profile field | Validation / behavior |
| --- | --- |
| `student_id` | Required in forms; at most 30 characters; not a unique database key. |
| `fields_of_study` | Required; at most 500 characters. |
| `classification` | Required: freshman, sophomore, junior, senior, graduate. |
| `level` | Required: undergrad or grad. |
| `credentials` | Optional text. |
| `experience` | Optional text. |
| `advertisement` | Optional employment-interest text on the profile, not a separate post. |
| `seeking_employment` | Boolean, default false; unchecked/omitted checkbox saves false. Only the owning student can edit through the profile route. |

Student signup submits account and profile fields without prefixes. It creates both records atomically and signs in the student. Profile editing uses `/accounts/profile/student/`, bound to the session owner; client-supplied owner IDs do not transfer ownership. A missing profile can be created there. Existing model allowances for blank IDs are preserved; the forms require them.

Faculty signup prefixes account fields with `user-` and profile fields with `profile-`. Faculty profile fields are `faculty_id` (required, maximum 30), `department` (optional, maximum 100), and `title` (required, maximum 100, displayed as Position). `is_approved` defaults false and is not exposed in signup/edit forms. The administrator approves records in `/admin/`. Approved faculty edit their own details at `/accounts/profile/faculty/`; pending faculty cannot edit there or browse student profiles or create jobs. Pending faculty may browse the general job list while signed in.

## Faculty profile browsing

`/accounts/students/` lists visible students ordered by username, showing name (falling back to username/email), fields of study and classification. Links use the Student database primary key, not the entered student ID.

`/accounts/students/<student_id>/` shows name/email fallback, fields of study, classification, level, credentials, experience, employment interests and seeking-employment status. The status indicator uses Django's `yesno` template filter. Because non-seeking profiles are hidden, accessible profiles show Yes. Student IDs are not displayed in these faculty views.

Both routes require approved faculty. Anonymous users redirect to login; signed-in unauthorized users receive 403. Hidden, inactive or nonexistent profiles return 404 to approved faculty. An empty list renders the existing empty-state message.

## Jobs

The homepage also renders saved postings inside the existing job-card section for signed-in users, using the same visibility rule as `/jobs/`. Anonymous visitors retain the original homepage placeholders; no posting details are disclosed. A signed-in user with no postings sees an empty-state message.

| Field | Validation / behavior |
| --- | --- |
| `title` | Required, maximum 255 characters. |
| `description` | Required text. |
| `start_date` | Required valid date. |
| `end_date` | Required valid date, on or after start date; also enforced by a database constraint. |
| `faculty` | Set by the server from the approved faculty session; not a form field. |
| `created_at` | Set by the database model when created; not a form field. |

GET `/jobs/create/` renders the form. A valid CSRF-protected POST saves the job and redirects to `/jobs/`; invalid fields render errors without saving. Anonymous, student, pending-faculty and faculty-without-profile requests receive 403. GET `/jobs/` requires login and renders all postings with title, description, faculty name (falling back to username) and start/end dates; an empty database renders the existing empty-state message.

## Storage and setup

`accounts.User` owns one Student or Faculty profile for the corresponding registration flow. A faculty User can own multiple JobPosting records. Profile and job foreign keys cascade on user deletion. The role/approval checks are enforced by the application views. SQLite is local; commit migrations, not database files. See README for installation, private key setup, migrations, admin creation and tests.

The sample-data command creates fictional users with unusable passwords, a student profile and one job. It is safe to repeat, but is not a substitute for registering and approving faculty in an interactive demo.

## Team acceptance checklist

Automated tests cover registration, invalid and duplicate inputs, sessions, admin approval, ownership, profile persistence and visibility, authorized posting and student retrieval, empty states, date validation, and missing CSRF rejection. Automated checks do not establish teammate acceptance.

- [ ] A teammate follows README in a fresh checkout/environment and starts Django.
- [ ] Spencer reviews the existing form routes, field contracts, navigation and error displays.
- [ ] Register a student; edit credentials/experience, log out, sign back in and confirm saved values.
- [ ] Register faculty; confirm privileged actions are denied until an admin approves the record; log out and sign back in after approval.
- [ ] Faculty opens the student list/detail; student turns seeking status off and on; faculty sees disappearance and reappearance with current details.
- [ ] Faculty creates a job; student sees it. Confirm invalid dates are rejected and a student cannot publish a job.
- [ ] Review the PR and record teammate acceptance on the corresponding Trello cards before moving them to Done.

Out of scope: applications, resume uploads, filtering, automatic closure, job editing/deletion, filled-position management and separate student advertisement posts.
