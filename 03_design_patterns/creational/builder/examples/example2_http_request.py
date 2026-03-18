# Advanced topic — validating mandatory fields inside build() so errors surface at construction time, not at use time.
"""
Builder Pattern — Example 2: HTTP Request Builder

Shows build()-time validation: URL is required and method must be a valid HTTP verb.
If either constraint is violated, build() raises ValueError before the object exists.

Real-world use: Razorpay's Python SDK assembles API requests this way — base URL and
auth key are mandatory, optional headers and retry settings added step by step, then
the request is validated and created only when build() is called.

Run: python example2_http_request.py
"""
from __future__ import annotations
from dataclasses import dataclass

VALID_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}


@dataclass
class HTTPRequest:
    """Immutable HTTP request. Created only by HTTPRequestBuilder.build()."""
    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, str]
    body: str | None
    timeout: int

    def __str__(self) -> str:
        return (f"{self.method} {self.url}\n"
                f"  Headers: {self.headers}  Params: {self.params}\n"
                f"  Body: {self.body!r}  Timeout: {self.timeout}s")


class HTTPRequestBuilder:
    """Fluent builder for HTTPRequest with validation on build()."""

    def __init__(self) -> None:
        self._method  = "GET"
        self._url     = ""
        self._headers: dict[str, str] = {}
        self._params:  dict[str, str] = {}
        self._body:    str | None = None
        self._timeout  = 60

    def method(self, m: str)           -> "HTTPRequestBuilder": self._method = m.upper(); return self
    def url(self, u: str)              -> "HTTPRequestBuilder": self._url = u;            return self
    def header(self, k: str, v: str)   -> "HTTPRequestBuilder": self._headers[k] = v;    return self
    def param(self, k: str, v: str)    -> "HTTPRequestBuilder": self._params[k] = v;     return self
    def body(self, b: str)             -> "HTTPRequestBuilder": self._body = b;           return self
    def timeout(self, t: int)          -> "HTTPRequestBuilder": self._timeout = t;        return self

    def build(self) -> HTTPRequest:
        """Validate mandatory fields, then produce the immutable HTTPRequest."""
        if not self._url:
            raise ValueError("URL must be set before calling build().")
        if self._method not in VALID_METHODS:
            raise ValueError(f"Invalid method '{self._method}'. Must be one of {sorted(VALID_METHODS)}.")
        return HTTPRequest(
            method=self._method, url=self._url,
            headers=dict(self._headers),  # snapshot
            params=dict(self._params),    # snapshot
            body=self._body, timeout=self._timeout,
        )


if __name__ == "__main__":
    get_req = (HTTPRequestBuilder()
               .url("https://api.razorpay.com/v1/payments")
               .header("Authorization", "Bearer key-abc")
               .param("count", "10")
               .timeout(30)
               .build())
    print("=== GET ===\n", get_req)

    post_req = (HTTPRequestBuilder()
                .method("POST")
                .url("https://api.razorpay.com/v1/orders")
                .header("Content-Type", "application/json")
                .body('{"amount": 50000, "currency": "INR"}')
                .build())
    print("\n=== POST ===\n", post_req)

    print("\n=== Validation ===")
    try:
        HTTPRequestBuilder().build()  # missing URL
    except ValueError as e:
        print(f"Missing URL  -> {e}")
    try:
        HTTPRequestBuilder().url("https://api.example.com").method("FETCH").build()
    except ValueError as e:
        print(f"Bad method   -> {e}")
