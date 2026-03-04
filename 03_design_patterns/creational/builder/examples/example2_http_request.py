"""
Builder Pattern — Example 2: HTTP Request Builder

Demonstrates:
- A dataclass product (HTTPRequest) with many optional fields
- An HTTPRequestBuilder with fluent setters that accumulate headers/params
- build() performing validation (URL required, method must be valid)
- Building a GET request and a POST request via method chaining
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

VALID_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}


@dataclass
class HTTPRequest:
    """
    Immutable representation of an HTTP request.
    Produced exclusively by HTTPRequestBuilder.build().
    """
    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, str]
    body: str | None
    timeout: int
    verify_ssl: bool

    def __str__(self) -> str:
        lines = [
            f"{self.method} {self.url}",
            f"  Headers   : {self.headers}",
            f"  Params    : {self.params}",
            f"  Body      : {self.body!r}",
            f"  Timeout   : {self.timeout}s",
            f"  Verify SSL: {self.verify_ssl}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class HTTPRequestBuilder:
    """
    Fluent builder for HTTPRequest objects.

    Usage (GET):
        req = (HTTPRequestBuilder()
               .method("GET")
               .url("https://api.example.com/users")
               .header("Accept", "application/json")
               .param("page", "1")
               .timeout(30)
               .build())

    Usage (POST):
        req = (HTTPRequestBuilder()
               .method("POST")
               .url("https://api.example.com/users")
               .header("Content-Type", "application/json")
               .body('{"name": "Alice"}')
               .build())
    """

    def __init__(self) -> None:
        self._method: str = "GET"
        self._url: str = ""
        self._headers: dict[str, str] = {}
        self._params: dict[str, str] = {}
        self._body: str | None = None
        self._timeout: int = 60
        self._verify_ssl: bool = True

    # --- fluent setters ---

    def method(self, m: str) -> HTTPRequestBuilder:
        self._method = m.upper()
        return self

    def url(self, u: str) -> HTTPRequestBuilder:
        self._url = u
        return self

    def header(self, key: str, value: str) -> HTTPRequestBuilder:
        """Add or overwrite a single request header."""
        self._headers[key] = value
        return self

    def param(self, key: str, value: str) -> HTTPRequestBuilder:
        """Add or overwrite a single query parameter."""
        self._params[key] = value
        return self

    def body(self, b: str) -> HTTPRequestBuilder:
        self._body = b
        return self

    def timeout(self, t: int) -> HTTPRequestBuilder:
        self._timeout = t
        return self

    def no_ssl_verify(self) -> HTTPRequestBuilder:
        """Disable SSL certificate verification (useful for local dev/testing)."""
        self._verify_ssl = False
        return self

    # --- terminal step with validation ---

    def build(self) -> HTTPRequest:
        """
        Validate and produce an immutable HTTPRequest.

        Raises:
            ValueError: if url is not set, or method is not a recognised HTTP verb.
        """
        if not self._url:
            raise ValueError("URL must be set before calling build().")
        if self._method not in VALID_METHODS:
            raise ValueError(
                f"Invalid HTTP method '{self._method}'. "
                f"Must be one of {sorted(VALID_METHODS)}."
            )
        return HTTPRequest(
            method=self._method,
            url=self._url,
            headers=dict(self._headers),   # snapshot
            params=dict(self._params),     # snapshot
            body=self._body,
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- GET request ---
    get_request = (HTTPRequestBuilder()
                   .method("GET")
                   .url("https://api.example.com/users")
                   .header("Accept", "application/json")
                   .header("Authorization", "Bearer token-abc123")
                   .param("page", "2")
                   .param("limit", "50")
                   .timeout(30)
                   .build())

    print("=== GET Request ===")
    print(get_request)

    print()

    # --- POST request (SSL verification disabled for local dev) ---
    post_request = (HTTPRequestBuilder()
                    .method("POST")
                    .url("https://localhost:8443/api/sessions")
                    .header("Content-Type", "application/json")
                    .header("X-API-Key", "secret-key")
                    .body('{"username": "alice", "password": "hunter2"}')
                    .timeout(10)
                    .no_ssl_verify()
                    .build())

    print("=== POST Request ===")
    print(post_request)

    # --- Validation demo ---
    print("\n=== Validation Examples ===")
    try:
        bad = HTTPRequestBuilder().method("GET").build()   # missing URL
    except ValueError as e:
        print(f"Missing URL  -> ValueError: {e}")

    try:
        bad = HTTPRequestBuilder().url("https://api.example.com").method("FETCH").build()
    except ValueError as e:
        print(f"Bad method   -> ValueError: {e}")
