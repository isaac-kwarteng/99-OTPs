import random

class VerifyAndSendSMS:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.otp = random.randint(1000, 9999)
         
    def send_otp(self):
        
        
