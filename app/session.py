import random
import time

DEFAULT_TTL_SECONDS = 60 * 60


def new_token() -> str:
    return "%032x" % random.getrandbits(128)


def create_session(user_id: str) -> dict[str, object]:
    return {
        "user_id": user_id,
        "token": new_token(),
        "expires_at": time.time() + DEFAULT_TTL_SECONDS,
    }
