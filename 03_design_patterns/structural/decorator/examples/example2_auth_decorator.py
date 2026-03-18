# Advanced topic — stacking auth and retry decorators on an HTTP API client
"""
Decorator Pattern - Example 2: Auth and Retry Decorators

APIClient provides get() and post() endpoints.
Two decorators are shown:
1. AuthenticatedAPIClient — injects an Authorization header on every call
2. RetryAPIClient — retries failed calls up to N times

Both are composable. Client code (UserAPI) is never changed.

Real-world use: Razorpay/Stripe SDK wrappers that inject API keys and
retry on 5xx responses without the business logic layer knowing about it.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
import time


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

@dataclass
class Response:
    status_code: int
    body: dict[str, Any]

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300


class APIError(Exception):
    pass


# ---------------------------------------------------------------------------
# Component Interface
# ---------------------------------------------------------------------------

class APIClient(ABC):
    @abstractmethod
    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response: ...

    @abstractmethod
    def post(self, endpoint: str, data: dict[str, Any],
             headers: Optional[dict] = None) -> Response: ...


# ---------------------------------------------------------------------------
# Concrete Component
# ---------------------------------------------------------------------------

class HttpAPIClient(APIClient):
    """Simulates a real HTTP client."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._requests_made = 0

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        self._requests_made += 1
        print(f"  [HTTP] GET {self._base_url}{endpoint} headers={headers or {}}")
        return Response(200, {"endpoint": endpoint, "data": {"id": 42}})

    def post(self, endpoint: str, data: dict[str, Any],
             headers: Optional[dict] = None) -> Response:
        self._requests_made += 1
        print(f"  [HTTP] POST {self._base_url}{endpoint} data={data}")
        return Response(201, {"created": True})

    @property
    def request_count(self) -> int:
        return self._requests_made


# ---------------------------------------------------------------------------
# Base Decorator
# ---------------------------------------------------------------------------

class APIClientDecorator(APIClient):
    """Forwards all calls to the wrapped client."""

    def __init__(self, wrapped: APIClient) -> None:
        self._wrapped = wrapped

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._wrapped.get(endpoint, headers)

    def post(self, endpoint: str, data: dict[str, Any],
             headers: Optional[dict] = None) -> Response:
        return self._wrapped.post(endpoint, data, headers)


# ---------------------------------------------------------------------------
# Decorator 1: Authentication
# ---------------------------------------------------------------------------

class AuthenticatedAPIClient(APIClientDecorator):
    """Injects an Authorization header into every request."""

    def __init__(self, wrapped: APIClient, token: str, scheme: str = "Bearer") -> None:
        super().__init__(wrapped)
        self._auth_header = f"{scheme} {token}"

    def _with_auth(self, headers: Optional[dict]) -> dict:
        merged = dict(headers or {})
        merged["Authorization"] = self._auth_header
        return merged

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._wrapped.get(endpoint, self._with_auth(headers))

    def post(self, endpoint: str, data: dict[str, Any],
             headers: Optional[dict] = None) -> Response:
        return self._wrapped.post(endpoint, data, self._with_auth(headers))


# ---------------------------------------------------------------------------
# Decorator 2: Retry
# ---------------------------------------------------------------------------

class RetryAPIClient(APIClientDecorator):
    """Retries failed requests up to max_retries times."""

    def __init__(self, wrapped: APIClient, max_retries: int = 3,
                 backoff_seconds: float = 0.1) -> None:
        super().__init__(wrapped)
        self._max_retries = max_retries
        self._backoff = backoff_seconds

    def _with_retry(self, operation):
        last_error: Optional[Exception] = None
        for attempt in range(1, self._max_retries + 2):
            try:
                return operation()
            except APIError as exc:
                last_error = exc
                if attempt <= self._max_retries:
                    wait = self._backoff * (2 ** (attempt - 1))
                    print(f"  [RETRY] Attempt {attempt} failed. Retrying in {wait:.2f}s")
                    time.sleep(wait)
        raise last_error

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._with_retry(lambda: self._wrapped.get(endpoint, headers))

    def post(self, endpoint: str, data: dict[str, Any],
             headers: Optional[dict] = None) -> Response:
        return self._with_retry(lambda: self._wrapped.post(endpoint, data, headers))


# ---------------------------------------------------------------------------
# Application code — only knows about APIClient
# ---------------------------------------------------------------------------

class UserAPI:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    def get_user(self, user_id: int) -> dict:
        return self._client.get(f"/users/{user_id}").body

    def create_user(self, name: str, email: str) -> dict:
        return self._client.post("/users", {"name": name, "email": email}).body


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = HttpAPIClient("https://api.example.com")

    # Stack: Retry → Auth → Http
    client = RetryAPIClient(
        AuthenticatedAPIClient(base, token="razorpay-secret-key"),
        max_retries=3,
    )
    api = UserAPI(client)

    print("--- GET user ---")
    print(api.get_user(1))

    print("\n--- POST create user ---")
    print(api.create_user("Alice", "alice@example.com"))

    print(f"\nBase HTTP requests made: {base.request_count}")
