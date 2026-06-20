from dataclasses import dataclass


@dataclass(frozen=True)
class ValidCredentials:
    email: str = "eve.holt@reqres.in"
    password: str = "cityslicka"


@dataclass(frozen=True)
class RegisterCredentials:
    email: str = "eve.holt@reqres.in"
    password: str = "pistol"


@dataclass(frozen=True)
class UnregisteredUser:
    email: str = "nobody@reqres.in"


@dataclass(frozen=True)
class NewUser:
    name: str = "morpheus"
    job: str = "leader"


@dataclass(frozen=True)
class UpdatedUser:
    name: str = "morpheus"
    job: str = "zion resident"


VALID_CREDS = ValidCredentials()
REGISTER_CREDS = RegisterCredentials()
UNREGISTERED_USER = UnregisteredUser()
NEW_USER = NewUser()
UPDATED_USER = UpdatedUser()

EXISTING_USER_ID = 2
NON_EXISTENT_USER_ID = 9999
VALID_PAGE = 1
INVALID_PAGE = 999
