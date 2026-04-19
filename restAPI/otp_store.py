import secrets
from datetime import datetime, timedelta

# In production, replace with Redis: redis.setex(phone, 300, otp)
_store: dict[str, dict] = {}

OTP_TTL_MINUTES = 2

def generate_and_store(phone_number: str) -> str:
    otp = str(secrets.randbelow(900000) + 100000)  # 6-digit, cryptographically secure
    _store[phone_number] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=OTP_TTL_MINUTES),
    }
    return otp

def verify_and_consume(phone_number: str, received_otp: str) -> bool:
    record = _store.get(phone_number)
    if not record:
        return False
    if datetime.utcnow() > record["expires_at"]:
        del _store[phone_number]  # clean up expired
        return False
    if record["otp"] == received_otp:
        del _store[phone_number]  # one-time use
        return True
    return False