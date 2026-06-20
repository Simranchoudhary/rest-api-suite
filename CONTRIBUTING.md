# Contributing

## Setup

```bash
make install
cp .env.example .env   # add your REQRES_API_KEY
```

## Running tests

```bash
make test              # full suite
make test-auth         # auth tests only
make test-users        # CRUD tests only
make test-contract     # contract tests only
make test-slow         # delayed-response / resilience tests
make report            # open HTML report in browser
```

## Linting

```bash
make lint              # check for issues
make lint-fix          # auto-fix where possible
```

All lint rules are defined in `pyproject.toml` under `[tool.ruff]`.

---

## Adding a new endpoint

### 1. Add a client method

If the endpoint belongs to an existing resource, add a method to the relevant client in `clients/`. If it's a new resource, create a new client that extends `BaseClient`.

```python
# clients/users_client.py
def search_users(self, query: str) -> Response:
    return self.get("/api/users/search", params={"q": query})
```

### 2. Add a JSON Schema

Create a schema file in `schemas/` named after the response shape:

```json
// schemas/search_results.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["results"],
  "properties": {
    "results": { "type": "array" },
    "_meta": { "$ref": "_meta.json" }
  },
  "additionalProperties": false
}
```

Always include `"_meta": { "$ref": "_meta.json" }` and `"additionalProperties": false` at the top level — reqres.in injects `_meta` on every response.

### 3. Add test data

Add any new credentials, IDs, or payloads as frozen dataclasses in `fixtures/test_data.py` and export them from `fixtures/__init__.py`. Never hardcode test data inside test files.

### 4. Write tests

| Test file | What goes here |
|---|---|
| `tests/test_auth.py` | Auth and registration flows |
| `tests/test_users.py` | User CRUD — functional assertions |
| `tests/test_contracts.py` | Schema validation — one test per endpoint |
| `tests/test_resilience.py` | Delayed responses, parametrized negative cases, edge inputs |

**Markers** — tag every test class with its marker:

```python
@pytest.mark.users
class TestSearchUsers:
    ...
```

Available markers: `auth`, `users`, `contract`, `slow`. Add new ones in `pyproject.toml` under `[tool.pytest.ini_options] markers`.

### 5. Contract test

Every new endpoint needs a contract test in `test_contracts.py`:

```python
def test_search_results_contract(self, users_client):
    response = users_client.search_users("george")
    assert response.status_code == 200
    validate_schema(response.json(), "search_results")
```

---

## Project conventions

- **No magic strings in tests** — all URLs live in clients, all test data lives in `fixtures/test_data.py`.
- **One assertion per test** where possible — makes failures immediately obvious.
- **Session-scoped fixtures** for clients and auth tokens — avoid re-authenticating on every test.
- **Parametrize negative cases** — use `@pytest.mark.parametrize` for table-driven invalid-input tests rather than writing one test per bad value.
- **Schema-first** — write the JSON Schema before writing the functional test. If the schema doesn't exist yet, the contract test will catch shape regressions from day one.
