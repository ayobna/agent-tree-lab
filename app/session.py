import random
import time

DEFAULT_TTL_SECONDS = 60 * 60
REMEMBER_ME_TTL_SECONDS = 60 * 60 * 24 * 30


def new_token() -> str:
    return "%032x" % random.getrandbits(128)


def create_session(user_id: str, remember_me: bool = False) -> dict[str, object]:
    ttl = REMEMBER_ME_TTL_SECONDS if remember_me else DEFAULT_TTL_SECONDS
    return {
        "user_id": user_id,
        "token": new_token(),
        "expires_at": time.time() + ttl,
    }
