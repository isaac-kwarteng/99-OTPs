import httpx
import os
import re
from dotenv import load_dotenv

load_dotenv()

SMS_API_URL = os.getenv("SMS_API_URL")
SMS_API_KEY = os.getenv("SMS_API_KEY")

def is_valid_phone(phone_number: str) -> bool:
    # Matches +233XXXXXXXXX or 0XXXXXXXXX (Ghana format)
    pattern = r"^(\+233|0)[2-9]\d{8}$"
    return bool(re.match(pattern, phone_number))

async def send_sms(phone_number: str, otp: str) -> bool:
    if not is_valid_phone(phone_number):
        raise ValueError(f"Invalid phone number: {phone_number}")
    
  
    SMS_SENDER_ID = os.getenv("SMS_SENDER_ID")
    
    payload = {
        "phone": [phone_number],
        "sender_id": SMS_SENDER_ID,
        "message": f"Your OTP is {otp}. It expires in 2 minutes. Do not share it with anyone."
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SMS_API_KEY}"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(SMS_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # raises on 4xx/5xx
            return True
        except httpx.HTTPStatusError as e:
            # e.g. 401 Unauthorized, 402 Payment Required (credits exhausted)
            print(f"SMS API error {e.response.status_code}: {e.response.text}")
            return False
        except httpx.RequestError as e:
            # Network-level failure: DNS, timeout, connection refused
            print(f"SMS request failed: {e}")
            return False