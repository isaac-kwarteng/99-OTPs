import secrets
import redis
import os
from dotenv import load_dotenv

load_dotenv()

OTP_TTL_SECONDS = 300  # 5 minutes

r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def generate_and_store(phone_number: str) -> str:
    otp = str(secrets.randbelow(900000) + 100000)
    r.setex(f"otp:{phone_number}", OTP_TTL_SECONDS, otp)  # key, TTL, value
    return otp

def verify_and_consume(phone_number: str, received_otp: str) -> bool:
    key = f"otp:{phone_number}"
    stored_otp = r.get(key)
    if not stored_otp:
        return False  # expired or never sent
    if stored_otp == received_otp:
        r.delete(key)  # consume — one time use
        return True
    return False