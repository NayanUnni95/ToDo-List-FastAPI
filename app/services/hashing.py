"""
This module provides hashing and validation functionality for passwords
using the `passlib` library.
"""

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
Hash:
    A utility class for hashing and validating passwords.
"""


class Hash:
    """
    Hashes a plaintext password using the bcrypt algorithm.
    """

    def bcrypt(password: str):
        return pwd_context.hash(password)

    """
    Verifies if a plaintext password matches a previously hashed password.
    """

    def validate(password: str, hashed_password: str):
        return pwd_context.verify(password, hashed_password)
