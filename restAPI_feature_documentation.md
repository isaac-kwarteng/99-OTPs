# 99-OTPs — REST API

A lightweight FastAPI service for sending and verifying one-time passwords (OTPs) via SMS. OTPs are 6 digits, expire after 2 minutes, and are single-use. Redis is used for state persistence.

---

## Tech stack

- **FastAPI** — API framework
- **Redis** — OTP storage with native TTL
- **httpx** — Async HTTP client for SMS delivery
- **uvicorn** — ASGI server
- **python-dotenv** — Environment variable management

---

## SMS provider

Bring your own. The `sms.py` module is the only file you need to touch — swap in your provider's API URL, key, and payload structure. Any provider that accepts an HTTP request works: Twilio, Africa's Talking, myCSMS, Termii, or anything else.

```python
# sms.py — update these to match your provider
SMS_API_URL = os.getenv("SMS_API_URL")
SMS_API_KEY = os.getenv("SMS_API_KEY")
SMS_SENDER_ID = os.getenv("SMS_SENDER_ID")

payload = {
    "phone": [phone_number],   # adjust field names to match your provider
    "sender_id": SMS_SENDER_ID,
    "message": f"Your OTP is {otp}. It expires in 2 minutes. Do not share it with anyone."
}
```

---

## Project structure

```
restAPI/
├── main.py               # FastAPI app and route handlers
├── otp_store.py          # Redis OTP storage, TTL, and verification
├── sms.py                # SMS delivery — swap provider here
├── schemas.py            # Pydantic request body models
├── .env                  # Environment variables (not committed)
├── requirements.txt      # Pinned dependencies
└── README.md
```

---

## Prerequisites

- Python 3.9+
- Redis installed and running

### Install Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl enable redis
sudo systemctl start redis

# verify
redis-cli ping  # should return PONG
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/99-OTPs.git
cd 99-OTPs/restAPI
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the `restAPI/` directory:
```env
SMS_API_URL=https://your-sms-provider.com/api/send
SMS_API_KEY=your_api_key
SMS_SENDER_ID=YourSenderID
REDIS_URL=redis://localhost:6379
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`.

---

## API reference

### POST `/otp/send`

Generates a 6-digit OTP and delivers it to the provided phone number via SMS.

**Request body**
```json
{
  "phone_number": "0512345678"
}
```

Accepts Ghana-format numbers: `0XXXXXXXXX` or `+233XXXXXXXXX`.

**Responses**

| Status | Body | Description |
|--------|------|-------------|
| 200 | `{ "message": "OTP sent" }` | OTP generated and sent successfully |
| 422 | `{ "detail": [...] }` | Request body missing or malformed |
| 502 | `{ "detail": "SMS delivery failed" }` | SMS provider rejected the request |

---

### POST `/otp/verify`

Validates the OTP for the given phone number. On success the OTP is consumed and cannot be reused.

**Request body**
```json
{
  "phone_number": "0512345678",
  "otp": "613166"
}
```

**Responses**

| Status | Body | Description |
|--------|------|-------------|
| 200 | `{ "success": true }` | OTP matched and consumed |
| 400 | `{ "detail": "Invalid or expired OTP" }` | OTP is wrong, expired, or already used |
| 422 | `{ "detail": [...] }` | Request body missing or malformed |

---

## How it works

1. Client calls `/otp/send` with a phone number
2. Server generates a cryptographically secure 6-digit OTP using Python's `secrets` module
3. OTP is stored in Redis under the key `otp:{phone_number}` with a 120-second TTL
4. OTP is delivered to the phone number via your configured SMS provider
5. Client calls `/otp/verify` with the phone number and received OTP
6. Server fetches the stored OTP from Redis and compares
7. On match, the key is deleted (one-time use) and `{ "success": true }` is returned
8. On mismatch or expiry, `400` is returned

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `SMS_API_URL` | Your SMS provider's API endpoint |
| `SMS_API_KEY` | Your SMS provider's Bearer token |
| `SMS_SENDER_ID` | Registered sender name or number |
| `REDIS_URL` | Redis connection URL |

**Production Redis URL with password:**
```env
REDIS_URL=redis://:yourpassword@127.0.0.1:6379
```

---

## Notes

- OTPs expire automatically after 2 minutes — Redis handles this natively, no cron job needed
- OTPs are single-use — the key is deleted immediately after a successful verification
- Phone validation enforces Ghana number format before any SMS is dispatched
- The SMS provider API key is never exposed to the client — all provider communication happens server-side
