from pwdlib import PasswordHash
from typing import Optional

# Reusable hashing context
password_ctx = PasswordHash.recommended()

# Hashed function for registration
def hash_password(password: str) -> str:
    return password_ctx.hash(password)

# Verify function used for login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_ctx.verify(plain_password, hashed_password)

# Advance verify and update outdated hash
def verify_and_update_password(plain_password: str, hashed_password: str) -> tuple[bool, Optional[str]]:
    return password_ctx.verify_and_update(plain_password, hashed_password)
