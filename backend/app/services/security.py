from pwdlib import PasswordHash
from typing import Optional

# Reusable hashing context
password_ctx = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hashes a plaintext password using pwdlib['Argon2']"""
    return password_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored hash"""
    return password_ctx.verify(plain_password, hashed_password)


def verify_and_update_password(
    plain_password: str, hashed_password: str
) -> tuple[bool, Optional[str]]:
    """Verifies a password and re-hashes it if the stored hash needs an update"""
    return password_ctx.verify_and_update(plain_password, hashed_password)
