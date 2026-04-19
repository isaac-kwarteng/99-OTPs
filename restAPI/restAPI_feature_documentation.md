# 99-OTPs

A lightweight FastAPI service for sending and verifying one-time passwords (OTPs) via SMS. OTPs are 6 digits, expire after 2 minutes, and are single-use. Redis is used for state persistence.

---

## Tech stack

- **FastAPI** — API framework
- **Redis** — OTP storage with native TTL
- **httpx** — Async HTTP client for SMS delivery
- **myCSMS** — SMS provider
- **uvicorn** — ASGI server
- **python-dotenv** — Environment variable management

---

## Project structure

```
99-OTPs/
├── main.py               # FastAPI app and route handlers
├── otp_store.py          # Redis OTP storage, TTL, and verification
├── sms.py                # SMS delivery via myCSMS API
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
cd 99-OTPs
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

Create a `.env` file in the project root:
```env
SMS_API_URL=https://app.mycsms.com/api/v3/sms/send
SMS_API_KEY=your_mycsms_api_key
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
4. OTP is delivered to the phone number via the myCSMS API
5. Client calls `/otp/verify` with the phone number and received OTP
6. Server fetches the stored OTP from Redis and compares
7. On match, the key is deleted (one-time use) and `{ "success": true }` is returned
8. On mismatch or expiry, `400` is returned

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `SMS_API_URL` | myCSMS API endpoint |
| `SMS_API_KEY` | myCSMS Bearer token |
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