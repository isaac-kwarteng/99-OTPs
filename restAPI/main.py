from fastapi import FastAPI

app = FastAPI()

@app.post("/otp/send")
def read_root():
    return {"Hello": "World"}
    
    
@app.post("/otp/verify")
def verify_otp():
    return {"Hello": "World"}
