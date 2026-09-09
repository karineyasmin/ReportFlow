"""
Authentication and Authorization dependencies using Keycloak JWT verification.
"""

from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import requests

from app.core import settings, logger

keycloak_realm_path = (
    f"{settings.KEYCLOAK_SERVER_URL.rstrip('/')}/realms/{settings.KEYCLOAK_REALM}"
)
public_keycloak_realm_path = (
    f"{settings.KEYCLOAK_PUBLIC_URL.rstrip('/')}/realms/{settings.KEYCLOAK_REALM}"
)
token_url = f"{public_keycloak_realm_path}/protocol/openid-connect/token"
certs_url = settings.KEYCLOAK_CERTS_URL or (
    f"{keycloak_realm_path}/protocol/openid-connect/certs"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

_jwks_cache: dict[str, Any] = {}


def get_keycloack_public_keys() -> dict[str, Any]:
    """
    Fetches JSON Web Key Sets (JWKS) containing public keys from Keycloak.
    Caches the result in memory to optimize performance.
    """
    global _jwks_cache
    if not _jwks_cache:
        try:
            response = requests.get(certs_url, timeout=10)
            response.raise_for_status()
            _jwks_cache = response.json()
            logger.info("Successfuly fetched public keys (JWKS) from Keycloak.")
        except requests.RequestException as exc:
            logger.error(f"Failed to fetch JWKS from Keycloak: {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to reach authentication server.",
            )

    return _jwks_cache


def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """
    Validates the JWT token signature and expiration using Keycloak's public keys.

    Returns the decoded token payload if valid.
    """
    jwks = get_keycloack_public_keys()

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header key ID (kid).",
            )

        payload = jwt.decode(
            token, key, algorithms=["RS256"], options={"verify_aud": False}
        )

        return payload

    except JWTError as exc:
        logger.warning(f"JWT Verification failed: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(required_role: str):
    """
    Role-Based Access Control (RBAC) dependecy factory.

    Ensures that decoded JWT contains the required Realm Role.
    """

    def role_checker(
        payload: dict[str, Any] = Depends(verify_jwt_token),
    ) -> dict[str, Any]:
        realm_access = payload.get("realm_access", {})
        roles = realm_access.get("roles", [])

        if required_role not in roles:
            logger.warning(
                f"Access denied. Required role '{required_role}' not found in user roles."
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required role: '{required_role}'",
            )
        return payload

    return role_checker
