# src/exceptions.py
from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication required", headers=None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not authorized", headers=None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found", headers=None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)
