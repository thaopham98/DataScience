from __future__ import annotations

from curl_cffi import requests

from config import DEFAULT_TIMEOUT, MAX_RETRIES, RESPONSE_ENCODING

IMPERSONATE_BROWSER = "chrome146"


def build_session() -> requests.Session:
    """A curl_cffi Session with a Chrome TLS/HTTP fingerprint and UTF-8 enforced on every response."""
    session = requests.Session(
        impersonate=IMPERSONATE_BROWSER,
        timeout=DEFAULT_TIMEOUT,
        retry=MAX_RETRIES,
    )

    # Force UTF-8 decoding for every response made through this session.
    original_get = session.get

    def get_utf8(*args, **kwargs):
        response = original_get(*args, **kwargs)
        response.encoding = RESPONSE_ENCODING
        return response

    session.get = get_utf8  # type: ignore[assignment]
    return session