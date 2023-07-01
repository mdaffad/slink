import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from shortener.config import settings

security = HTTPBasic()


def is_authorized(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    current_username_bytes = credentials.username.encode("utf8")
    print(credentials.username)
    correct_username_bytes = settings.BASIC_AUTH_USERNAME.get_secret_value().encode(
        "utf-8"
    )
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = settings.BASIC_AUTH_PASSWORD.get_secret_value().encode(
        "utf-8"
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        return False

    return True


async def secure_api_access(is_authorized: bool = Depends(is_authorized)) -> None:
    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
