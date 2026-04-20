from fastapi import FastAPI, HTTPException
from schemas import SendOTPRequest, VerifyOTPRequest
from sms import send_sms          # your httpx logic, isolated
import otp_store

app = FastAPI()

@app.post("/otp/send")
async def send_otp(body: SendOTPRequest):
    otp = otp_store.generate_and_store(body.phone_number)
    success = await send_sms(body.phone_number, otp)
    if not success:
        raise HTTPException(502, "SMS delivery failed")
    return {"message": "OTP sent"}   

@app.post("/otp/verify")
async def verify_otp(body: VerifyOTPRequest):
    valid = otp_store.verify_and_consume(body.phone_number, body.otp)
    if not valid:
        raise HTTPException(400, "Invalid or expired OTP")
    return {"success": True}