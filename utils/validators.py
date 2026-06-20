import json
from pathlib import Path
import jsonschema
from jsonschema import ValidationError
from jsonschema.validators import validator_for
import referencing
from referencing import Registry, Resource


SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


def _build_registry() -> Registry:
    resources = []
    for schema_file in SCHEMAS_DIR.glob("*.json"):
        content = json.loads(schema_file.read_text())
        uri = schema_file.name
        resources.append((uri, Resource.from_contents(content)))
    return Registry().with_resources(resources)


_REGISTRY = _build_registry()


def load_schema(schema_name: str) -> dict:
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text())


def validate_schema(payload: dict, schema_name: str) -> None:
    schema = load_schema(schema_name)
    cls = validator_for(schema)
    validator = cls(schema, registry=_REGISTRY)
    errors = list(validator.iter_errors(payload))
    if errors:
        exc = errors[0]
        raise AssertionError(
            f"Schema validation failed for '{schema_name}':\n"
            f"  Path:    {' -> '.join(str(p) for p in exc.absolute_path) or '<root>'}\n"
            f"  Message: {exc.message}"
        )


def assert_response_time(response, max_ms: int = 2000) -> None:
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms <= max_ms, (
        f"Response too slow: {elapsed_ms:.0f}ms (limit {max_ms}ms)"
    )
