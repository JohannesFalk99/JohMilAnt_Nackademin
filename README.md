# School Lunch System

A school project built by Johannes, Milad and Antonio at Nackademin. Students can browse meals, place orders and submit ratings through a Flask web interface. The application stores students, meals and orders in SQLite.

The project uses Python, Flask, SQLite and Requests. Docker Compose provides a local setup, and GitHub Actions runs the automated tests and checks container startup.

## Run locally

Use Python 3.12. From the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python launch_application.py
```

Open http://127.0.0.1:5000 and enter a sample student name, such as `Alice Johansson`, with password `school-lunch-demo`. This shared password is only for sample data.

The launcher creates sample data when `test.db` is missing. To replace local sample data:

```bash
python create_sample_database.py --reset
```

## Run with Docker

```bash
cp .env.example .env
python -c 'import secrets; print(secrets.token_hex(32))'
```

Paste the generated value after `SECRET_KEY=` in `.env`, then run:

```bash
docker compose up --build
```

Open http://127.0.0.1:5000. A fresh database uses the same sample login shown above. SQLite data is stored in the `lunch-data` volume and survives container restarts. The container runs as a non-root user and serves the application with Gunicorn.

## How it works

The browser sends requests to Flask. Routes in `web_interface/flask_server.py` use `SchoolLunchDB`, which accesses SQLite through `database_wrapper.py`. Meal imports use `skolmaten_api.py` to query Open Food Facts. The external API is optional for browsing and ordering sample meals.

| File | Purpose |
| --- | --- |
| `web_interface/flask_server.py` | Web routes, session handling and JSON endpoints |
| `web_interface/templates/` | Login and meal dashboard |
| `lunch_system_database.py` | Schema, meals, students, orders and ratings |
| `database_wrapper.py` | SQLite connections and queries |
| `create_sample_database.py` | Sample students, meals and transactions |
| `launch_application.py` | Local startup |
| `tests/automated/` | Automated checks using temporary databases |

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover login, logout, access checks, meal listing, orders and ratings without calling external APIs. Older scripts in `tests/` are manual diagnostics and are excluded from pytest collection.

GitHub Actions runs the tests, builds the Docker image and checks that the container responds to HTTP requests on pushes and pull requests.

## Configuration

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Required secret used to sign session cookies |
| `DATABASE_PATH` | SQLite file location; defaults to `test.db` in the project directory |
| `SESSION_COOKIE_SECURE` | Set to `true` when using HTTPS; defaults to `false` for local HTTP |
| `FLASK_DEBUG` | Set to `1` only for local debugging; disabled by default |

Docker Compose reads `.env`. For direct Python startup, export variables in the shell. Keep `.env` and generated databases out of commits.

## Current limitations

Login requires a student name and password. Passwords are stored as salted hashes, and login, logout and POST API requests use CSRF protection. This is still a local learning demo: sample accounts share a publicly documented password. Do not use it with real student data or expose it publicly.

Role-based permissions, login rate limiting and deployment hardening are still needed before deployment. Allergy information is stored, but meals are not automatically filtered by allergies. Administrative database operations are available in Python and command-line scripts; the web interface does not provide a separate admin role.

## Existing databases

Existing students do not get automatic passwords. The application adds a credentials table without deleting students, meals or orders. Set a password for each account you want to use:

```bash
python set_student_password.py --name "Alice Johansson"
```

The command prompts locally and stores a hash. For a custom database, add `--database path/to/lunch.db`. To regenerate disposable sample data instead, run `python create_sample_database.py --reset`; this deletes the old local data.

Sessions created before password authentication was added are rejected. Existing Docker volumes keep their data; run the password command inside the container:

```bash
docker compose exec web python set_student_password.py --name "Alice Johansson"
```

## Milad's recent work

Milad added the Docker setup, automated tests and GitHub Actions workflow, fixed fresh database setup, and simplified the documentation in [pull request #6](https://github.com/JohannesFalk99/JohMilAnt_Nackademin/pull/6). The original application was built as a group project.

## CI status

The workflow is configured to run tests and check container startup. GitHub currently prevents jobs from starting because the repository owner's account is locked due to a billing issue. The owner must resolve that in GitHub billing before CI can run. Local tests can still be run using the command above.

## Team

Johannes ([JohannesFalk99](https://github.com/JohannesFalk99)), Milad ([miladlit](https://github.com/miladlit)) and Antonio.
