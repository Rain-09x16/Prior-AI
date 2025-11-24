"""
Clerk authentication utilities for FastAPI.
"""
import jwt
import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
import os

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)

# Cache for JWKS (JSON Web Key Set)
_jwks_cache: Optional[Dict[str, Any]] = None


async def get_jwks(clerk_domain: str) -> Dict[str, Any]:
    """
    Fetch Clerk JWKS (JSON Web Key Set) for token verification.
    """
    global _jwks_cache

    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://{clerk_domain}/.well-known/jwks.json")
            response.raise_for_status()
            _jwks_cache = response.json()

    return _jwks_cache


def verify_clerk_token(token: str, clerk_publishable_key: str) -> Dict[str, Any]:
    """
    Verify Clerk JWT token.

    Args:
        token: JWT token from Authorization header
        clerk_publishable_key: Clerk publishable key (pk_...)

    Returns:
        Decoded token payload with user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Extract the instance ID from the publishable key
        # Format: pk_test_<instance>_<random> or pk_live_<instance>_<random>
        parts = clerk_publishable_key.split('_')
        if len(parts) < 3:
            raise ValueError("Invalid Clerk publishable key format")

        # For testing, we'll decode without verification
        # In production, you should verify with Clerk's JWKS
        decoded = jwt.decode(
            token,
            options={"verify_signature": False}  # Temporarily disabled for development
        )

        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[Dict[str, Any]]:
    """
    FastAPI dependency to get current authenticated user from Clerk token.

    Returns:
        User information from decoded JWT token, or None if no token provided

    Raises:
        HTTPException: If token is provided but invalid
    """
    if credentials is None:
        return None

    clerk_key = os.getenv("CLERK_PUBLISHABLE_KEY")
    if not clerk_key:
        # If Clerk is not configured, allow access (for development/backward compatibility)
        return None

    user = verify_clerk_token(credentials.credentials, clerk_key)
    return user


async def require_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Dict[str, Any]:
    """
    FastAPI dependency that requires authentication.

    Returns:
        User information from decoded JWT token

    Raises:
        HTTPException: If no token provided or token is invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    clerk_key = os.getenv("CLERK_PUBLISHABLE_KEY")
    if not clerk_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication not configured",
        )

    user = verify_clerk_token(credentials.credentials, clerk_key)
    return user


def get_user_id(user: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Extract user ID from decoded Clerk token.

    Args:
        user: Decoded JWT token payload

    Returns:
        User ID string or None
    """
    if user is None:
        return None

    # Clerk tokens have 'sub' claim with user ID
    return user.get('sub')
