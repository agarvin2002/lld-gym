"""
Decorator Pattern - Example 2: Auth, Retry, and Rate-Limiting Decorators

Scenario:
    APIClient provides get() and post() endpoints.
    We need to add:
    1. Authentication: inject Authorization header on every call
    2. Retry: retry failed calls up to N times
    3. Rate Limiting: enforce a minimum interval between calls

    All three are composable decorators — the client code never changes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
import time
import random


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

@dataclass
class Response:
    status_code: int
    body: dict[str, Any]
    headers: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    def __str__(self) -> str:
        return f"Response({self.status_code}, body={self.body})"


class APIError(Exception):
    """Raised when an API call fails."""
    pass


# ---------------------------------------------------------------------------
# Component Interface
# ---------------------------------------------------------------------------

class APIClient(ABC):
    """Abstract interface for an HTTP API client."""

    @abstractmethod
    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        """Perform a GET request."""
        ...

    @abstractmethod
    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        """Perform a POST request."""
        ...


# ---------------------------------------------------------------------------
# Concrete Component
# ---------------------------------------------------------------------------

class HttpAPIClient(APIClient):
    """
    Simulates a real HTTP client.
    In a real implementation this would use requests / httpx / aiohttp.
    """

    def __init__(self, base_url: str, failure_rate: float = 0.0) -> None:
        self._base_url = base_url
        self._failure_rate = failure_rate  # 0.0–1.0 for simulating flaky network
        self._requests_made = 0

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        self._requests_made += 1
        self._maybe_fail(endpoint)
        print(f"  [HTTP] GET {self._base_url}{endpoint} headers={headers or {}}")
        return Response(
            status_code=200,
            body={"endpoint": endpoint, "data": {"id": 42, "value": "sample"}},
            headers={"Content-Type": "application/json"},
        )

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        self._requests_made += 1
        self._maybe_fail(endpoint)
        print(f"  [HTTP] POST {self._base_url}{endpoint} headers={headers or {}} data={data}")
        return Response(
            status_code=201,
            body={"created": True, "id": random.randint(100, 999)},
            headers={"Content-Type": "application/json"},
        )

    def _maybe_fail(self, endpoint: str) -> None:
        if random.random() < self._failure_rate:
            raise APIError(f"Network error on {endpoint}")

    @property
    def request_count(self) -> int:
        return self._requests_made


# ---------------------------------------------------------------------------
# Base Decorator
# ---------------------------------------------------------------------------

class APIClientDecorator(APIClient):
    """Base decorator — forwards all calls to the wrapped client."""

    def __init__(self, wrapped: APIClient) -> None:
        self._wrapped = wrapped

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._wrapped.get(endpoint, headers)

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        return self._wrapped.post(endpoint, data, headers)


# ---------------------------------------------------------------------------
# Decorator 1: Authentication
# ---------------------------------------------------------------------------

class AuthenticatedAPIClient(APIClientDecorator):
    """
    Injects an Authorization header into every request.
    Supports Bearer token, Basic, and API Key schemes.
    """

    def __init__(self, wrapped: APIClient, token: str, scheme: str = "Bearer") -> None:
        super().__init__(wrapped)
        self._auth_header = f"{scheme} {token}"

    def _inject_auth(self, headers: Optional[dict]) -> dict:
        merged = dict(headers or {})
        merged["Authorization"] = self._auth_header
        return merged

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._wrapped.get(endpoint, self._inject_auth(headers))

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        return self._wrapped.post(endpoint, data, self._inject_auth(headers))


# ---------------------------------------------------------------------------
# Decorator 2: Retry
# ---------------------------------------------------------------------------

class RetryAPIClient(APIClientDecorator):
    """
    Retries failed requests up to max_retries times with exponential backoff.
    Only retries on APIError (transient network failures).
    """

    def __init__(
        self,
        wrapped: APIClient,
        max_retries: int = 3,
        backoff_seconds: float = 0.1,
    ) -> None:
        super().__init__(wrapped)
        self._max_retries = max_retries
        self._backoff = backoff_seconds

    def _with_retry(self, operation):
        last_error: Optional[Exception] = None
        for attempt in range(1, self._max_retries + 2):  # +2: initial + retries
            try:
                return operation()
            except APIError as exc:
                last_error = exc
                if attempt <= self._max_retries:
                    wait = self._backoff * (2 ** (attempt - 1))
                    print(f"  [RETRY] Attempt {attempt} failed: {exc}. Retrying in {wait:.2f}s")
                    time.sleep(wait)
                else:
                    print(f"  [RETRY] All {self._max_retries + 1} attempts failed.")
        raise last_error  # re-raise after all retries exhausted

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        return self._with_retry(lambda: self._wrapped.get(endpoint, headers))

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        return self._with_retry(lambda: self._wrapped.post(endpoint, data, headers))


# ---------------------------------------------------------------------------
# Decorator 3: Rate Limiting
# ---------------------------------------------------------------------------

class RateLimitedAPIClient(APIClientDecorator):
    """
    Enforces a minimum interval between consecutive API calls.
    If a call comes in too soon, it sleeps until the interval has passed.
    """

    def __init__(self, wrapped: APIClient, min_interval_ms: float = 100) -> None:
        super().__init__(wrapped)
        self._min_interval = min_interval_ms / 1000.0  # convert to seconds
        self._last_call_time: float = 0.0
        self._throttled_count = 0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_call_time
        if elapsed < self._min_interval:
            wait = self._min_interval - elapsed
            print(f"  [RATE LIMIT] Throttling for {wait * 1000:.1f}ms")
            self._throttled_count += 1
            time.sleep(wait)
        self._last_call_time = time.monotonic()

    def get(self, endpoint: str, headers: Optional[dict] = None) -> Response:
        self._throttle()
        return self._wrapped.get(endpoint, headers)

    def post(
        self,
        endpoint: str,
        data: dict[str, Any],
        headers: Optional[dict] = None,
    ) -> Response:
        self._throttle()
        return self._wrapped.post(endpoint, data, headers)

    @property
    def throttled_count(self) -> int:
        return self._throttled_count


# ---------------------------------------------------------------------------
# Application code — only knows about APIClient
# ---------------------------------------------------------------------------

class UserAPI:
    """High-level API wrapper. Uses APIClient interface — unaware of decorators."""

    def __init__(self, client: APIClient) -> None:
        self._client = client

    def get_user(self, user_id: int) -> dict:
        response = self._client.get(f"/users/{user_id}")
        if not response.ok:
            raise ValueError(f"Failed to get user: {response.status_code}")
        return response.body

    def create_user(self, name: str, email: str) -> dict:
        response = self._client.post("/users", {"name": name, "email": email})
        if not response.ok:
            raise ValueError(f"Failed to create user: {response.status_code}")
        return response.body


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)
    print("=" * 60)
    print("DECORATOR PATTERN - Auth, Retry, Rate-Limiting Demo")
    print("=" * 60)

    # --- 1. Plain client ---
    print("\n--- 1. Plain HttpAPIClient ---")
    plain = HttpAPIClient("https://api.example.com")
    api = UserAPI(plain)
    print(api.get_user(1))

    # --- 2. Auth only ---
    print("\n--- 2. AuthenticatedAPIClient ---")
    authed = AuthenticatedAPIClient(
        HttpAPIClient("https://api.example.com"),
        token="my-secret-jwt-token",
    )
    api2 = UserAPI(authed)
    print(api2.get_user(2))
    api2.create_user("Alice", "alice@example.com")

    # --- 3. Full stack: RateLimit → Retry → Auth → HttpClient ---
    print("\n--- 3. Full Stack: RateLimited(Retry(Authenticated(Http))) ---")
    base = HttpAPIClient("https://api.example.com", failure_rate=0.0)
    stacked = RateLimitedAPIClient(
        RetryAPIClient(
            AuthenticatedAPIClient(base, token="stack-token"),
            max_retries=3,
        ),
        min_interval_ms=50,
    )
    api3 = UserAPI(stacked)

    print("\nMaking rapid calls (rate limiter will kick in):")
    for i in range(1, 4):
        result = api3.get_user(i)
        print(f"  user {i} →", result.get("data", {}))

    print(f"\nThrottled calls: {stacked.throttled_count}")
    print(f"Base HTTP requests made: {base.request_count}")

    # --- 4. Retry under flaky network ---
    print("\n--- 4. RetryAPIClient with flaky network (30% failure rate) ---")
    random.seed(0)
    flaky_base = HttpAPIClient("https://flaky.example.com", failure_rate=0.4)
    retried = RetryAPIClient(
        AuthenticatedAPIClient(flaky_base, token="retry-token"),
        max_retries=3,
        backoff_seconds=0.01,
    )
    api4 = UserAPI(retried)
    try:
        result = api4.get_user(99)
        print("  Succeeded:", result)
    except APIError as e:
        print(f"  All retries exhausted: {e}")

    print("\nDone.")
