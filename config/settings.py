import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Environment:
    base_url: str
    timeout: int
    verify_ssl: bool


ENVIRONMENTS = {
    "dev": Environment(
        base_url="https://reqres.in",
        timeout=10,
        verify_ssl=True,
    ),
    "staging": Environment(
        base_url="https://reqres.in",
        timeout=15,
        verify_ssl=True,
    ),
    "prod": Environment(
        base_url="https://reqres.in",
        timeout=20,
        verify_ssl=True,
    ),
}


def get_env() -> Environment:
    env_name = os.getenv("TEST_ENV", "dev")
    if env_name not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment '{env_name}'. Choose from: {list(ENVIRONMENTS)}")
    return ENVIRONMENTS[env_name]
