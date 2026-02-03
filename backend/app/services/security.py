from pwdlib import PasswordHash
from typing import Optional
import secrets
import string
import random
import os

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


def token_secret_retrival() -> str:
    """Retrieve or generate the secret key for JWT signing"""
    secret_token = secrets.token_hex(20)
    return secret_token


def token_algorithim_retrival() -> str:
    """Return the algorithm used for JWT signing"""
    return "HS256"


def token_string_randomizer(length: int = 16) -> str:
    """Generate a random string for JTI or other security purposes"""
    charaters = string.ascii_letters + string.digits
    return "".join(random.choice(charaters) for _ in range(length))


def get_secret_key() -> str:
    """Get the secret key from environment variables"""
    secret_key = os.getenv("SECRET_TOKEN")
    return secret_key
