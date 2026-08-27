import time

from app.session import DEFAULT_TTL_SECONDS, create_session


def test_token_is_32_hex_chars() -> None:
    token = create_session("u1")["token"]
    assert isinstance(token, str)
    assert len(token) == 32
    int(token, 16)


def test_default_ttl_is_one_hour() -> None:
    expires_at = create_session("u1")["expires_at"]
    assert isinstance(expires_at, float)
    assert 0 < expires_at - time.time() <= DEFAULT_TTL_SECONDS
