# REST API Automation Suite

[![CI](https://github.com/Simranchoudhary/rest-api-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/Simranchoudhary/rest-api-suite/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Tests](https://img.shields.io/badge/tests-76%20passing-brightgreen)

A senior-level API test automation framework built with Python, Requests, and PyTest — covering auth flows, user CRUD workflows, error-case validation, JSON Schema contract testing, SLA assertions, and resilience testing across multiple environments.

---

## Tech Stack

- **Python 3.11+**
- **Requests** — HTTP client
- **PyTest** — test runner
- **jsonschema** — JSON Schema contract validation
- **pytest-html** — HTML test reports
- **pytest-retry** — automatic retry on flaky network conditions
- **python-dotenv** — environment config
- **Ruff** — linting and import sorting

---

## Project Structure

```
rest-api-suite/
├── .github/
│   ├── workflows/ci.yml                        # GitHub Actions — lint + test on push/PR
│   └── PULL_REQUEST_TEMPLATE/
│       └── pull_request_template.md
├── clients/
│   ├── base_client.py                          # Shared session, headers, timeout, SSL config
│   ├── auth_client.py                          # Login and register endpoints
│   └── users_client.py                         # Full CRUD — list, get, create, put, patch, delete
├── config/
│   └── settings.py                             # Multi-env config (dev / staging / prod)
├── fixtures/
│   └── test_data.py                            # Typed test data — no magic strings in tests
├── schemas/
│   ├── _meta.json                              # Shared reqres.in metadata schema ($ref target)
│   ├── auth_login.json
│   ├── auth_register.json
│   ├── user.json
│   ├── users_list.json
│   └── created_user.json
├── tests/
│   ├── conftest.py                             # Session-scoped fixtures and auth token setup
│   ├── test_auth.py                            # 17 auth tests
│   ├── test_users.py                           # 29 CRUD tests
│   ├── test_contracts.py                       # 13 contract/schema tests
│   └── test_resilience.py                      # 17 delayed response + parametrized edge cases
├── utils/
│   └── validators.py                           # Schema validation + response time assertion
├── reports/                                    # HTML reports (git-ignored)
├── .env.example
├── Makefile
├── pyproject.toml                              # All config: deps, pytest, ruff
└── CONTRIBUTING.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Simranchoudhary/rest-api-suite.git
cd rest-api-suite
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
TEST_ENV=dev                          # dev | staging | prod
REQRES_API_KEY=your_key_here          # Free key from https://app.reqres.in/api-keys
```

---

## Running Tests

```bash
make test              # all 76 tests
make test-auth         # auth and registration tests
make test-users        # user CRUD tests
make test-contract     # JSON Schema contract tests
make test-slow         # delayed response / resilience tests
make lint              # ruff lint check
make report            # open HTML report in browser
```

Or run pytest directly:

```bash
pytest -x              # stop on first failure
pytest -v --tb=long    # verbose with full tracebacks
```

HTML report is generated automatically at `reports/report.html`:

```bash
open reports/report.html
```

---

## Test Coverage

| Area | Tests | What's covered |
|---|---|---|
| **Auth — Login** | 10 | 200 + token shape, schema, response time, missing password, unregistered user, empty body, token consistency |
| **Auth — Register** | 7 | 200 + id/token, schema, missing password, unregistered email |
| **Users — List** | 9 | 200, schema, pagination, empty page, totals consistency, response time, field presence |
| **Users — Get** | 6 | 200, schema, ID match, 404, empty body on 404, response time |
| **Users — Create** | 7 | 201, schema, name/job match, ID present, createdAt present, response time |
| **Users — Update** | 7 | PUT 200, name/job updated, updatedAt; PATCH 200, partial update, updatedAt |
| **Users — Delete** | 2 | 204, empty body |
| **Contracts** | 13 | Schema validation for every endpoint; parametrized across all user IDs 1–6 |
| **Resilience** | 17 | SLA under artificial delay, parametrized invalid logins, null/empty/max-length inputs, negative user IDs |

---

## Architecture

### Client Layer

Each client extends `BaseClient`, which manages a shared `requests.Session` with:
- API key injection via `x-api-key` header
- Optional Bearer token for authenticated requests
- Per-environment timeout and SSL settings

### Multi-Environment Config

Set `TEST_ENV` in `.env` to switch between environments. Each environment defines its own `base_url`, `timeout`, and `verify_ssl`:

```python
ENVIRONMENTS = {
    "dev":     Environment(base_url="https://reqres.in", timeout=10, ...),
    "staging": Environment(base_url="https://reqres.in", timeout=15, ...),
    "prod":    Environment(base_url="https://reqres.in", timeout=20, ...),
}
```

### Contract Testing

Every schema lives in `schemas/` as a JSON Schema Draft-07 file. The `validate_schema()` utility resolves `$ref` cross-references and raises a descriptive `AssertionError` on failure — pinpointing the exact field path that broke.

### Fixtures

Test data is defined as frozen dataclasses in `fixtures/test_data.py`. PyTest fixtures in `conftest.py` are session-scoped — the auth token is fetched once and reused across all tests that need it.

---

## API Under Test

This suite tests the public [reqres.in](https://reqres.in) API — a hosted REST API designed for frontend and QA testing. A free API key is required: [app.reqres.in/api-keys](https://app.reqres.in/api-keys).
